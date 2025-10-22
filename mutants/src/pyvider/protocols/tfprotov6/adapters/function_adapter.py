# pyvider/protocols/tfprotov6/adapters/function_adapter.py
import json
from typing import Any

from provide.foundation import logger

# FIX: Import the type encoder from its new, correct location in pyvider.cty
from pyvider.cty.conversion.type_encoder import encode_cty_type_to_wire_json
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


def x_dict_to_proto_function__mutmut_orig(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_1(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = None
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_2(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get(None, "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_3(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", None)
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_4(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_5(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", )
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_6(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("XXnameXX", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_7(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("NAME", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_8(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "XXunknownXX")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_9(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "UNKNOWN")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_10(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = None
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_11(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get(None, []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_12(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", None):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_13(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get([]):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_14(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", ):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_15(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("XXparametersXX", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_16(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("PARAMETERS", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_17(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = None
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_18(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get(None)
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_19(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("XXcty_typeXX")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_20(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("CTY_TYPE")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_21(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is not None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_22(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    None
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_23(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get(None)}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_24(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('XXnameXX')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_25(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('NAME')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_26(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = None

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_27(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = None

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_28(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode(None)

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_29(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(None).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_30(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(None)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_31(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("XXutf-8XX")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_32(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("UTF-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_33(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                None
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_34(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=None,
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_35(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=None,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_36(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=None,
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_37(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=None,
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_38(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=None,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_39(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_40(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_41(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_42(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_43(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_44(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get(None, ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_45(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", None),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_46(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get(""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_47(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_48(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("XXnameXX", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_49(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("NAME", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_50(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", "XXXX"),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_51(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get(None, ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_52(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", None),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_53(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get(""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_54(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_55(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("XXdescriptionXX", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_56(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("DESCRIPTION", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_57(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", "XXXX"),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_58(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get(None, False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_59(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", None),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_60(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get(False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_61(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", ),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_62(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("XXallow_nullXX", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_63(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("ALLOW_NULL", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_64(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", True),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_65(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=False,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_66(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = ""
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_67(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get(None):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_68(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("XXvariadic_parameterXX"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_69(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("VARIADIC_PARAMETER"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_70(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = None
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_71(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get(None)
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_72(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("XXcty_typeXX")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_73(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("CTY_TYPE")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_74(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is not None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_75(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    None
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_76(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get(None)}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_77(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('XXnameXX')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_78(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('NAME')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_79(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = None

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_80(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = None

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_81(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode(None)

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_82(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(None).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_83(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(None)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_84(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("XXutf-8XX")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_85(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("UTF-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_86(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = None

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_87(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=None,
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_88(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=None,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_89(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=None,
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_90(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=None,
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_91(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=None,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_92(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_93(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_94(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_95(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_96(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_97(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get(None, "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_98(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", None),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_99(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_100(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", ),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_101(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("XXnameXX", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_102(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("NAME", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_103(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "XXoptionsXX"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_104(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "OPTIONS"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_105(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get(None, "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_106(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", None),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_107(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_108(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", ),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_109(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("XXdescriptionXX", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_110(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("DESCRIPTION", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_111(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "XXOptional parametersXX"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_112(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_113(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "OPTIONAL PARAMETERS"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_114(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get(None, True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_115(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", None),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_116(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get(True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_117(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", ),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_118(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("XXallow_nullXX", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_119(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("ALLOW_NULL", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_120(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", False),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_121(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=False,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_122(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = ""
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_123(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get(None):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_124(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("XXreturnXX"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_125(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("RETURN"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_126(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = None
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_127(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get(None)
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_128(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("XXcty_typeXX")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_129(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("CTY_TYPE")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_130(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is not None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_131(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    None
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_132(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = None

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_133(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = None
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_134(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode(None)
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_135(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(None).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_136(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(None)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_137(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("XXutf-8XX")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_138(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("UTF-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_139(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = None
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_140(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=None)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_141(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                None
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_142(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = None
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_143(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = None
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_144(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode(None)
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_145(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(None).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_146(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(None)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_147(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("XXutf-8XX")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_148(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("UTF-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_149(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = None

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_150(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=None)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_151(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = None

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_152(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "XXparametersXX": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_153(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "PARAMETERS": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_154(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "XXsummaryXX": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_155(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "SUMMARY": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_156(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get(None, ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_157(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", None),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_158(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get(""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_159(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_160(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("XXsummaryXX", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_161(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("SUMMARY", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_162(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", "XXXX"),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_163(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "XXdescriptionXX": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_164(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "DESCRIPTION": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_165(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get(None, ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_166(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", None),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_167(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get(""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_168(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_169(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("XXdescriptionXX", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_170(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("DESCRIPTION", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_171(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", "XXXX"),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_172(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "XXdeprecation_messageXX": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_173(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "DEPRECATION_MESSAGE": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_174(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get(None, ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_175(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", None),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_176(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get(""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_177(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_178(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("XXdeprecation_messageXX", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_179(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("DEPRECATION_MESSAGE", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_180(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", "XXXX"),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_181(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = None

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_182(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["XXvariadic_parameterXX"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_183(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["VARIADIC_PARAMETER"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_184(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = None

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_185(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["XXreturnXX"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_186(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["RETURN"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_187(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(None, exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_188(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=None)
        return None


def x_dict_to_proto_function__mutmut_189(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(exc_info=True)
        return None


def x_dict_to_proto_function__mutmut_190(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", )
        return None


def x_dict_to_proto_function__mutmut_191(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        # Process required parameters
        parameters = []
        for param_data in func_data.get("parameters", []):
            cty_type_obj = param_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for parameter '{param_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            parameters.append(
                pb.Function.Parameter(
                    name=param_data.get("name", ""),
                    type=type_bytes,
                    description=param_data.get("description", ""),
                    allow_null_value=param_data.get("allow_null", False),
                    allow_unknown_values=True,
                )
            )

        # Process variadic parameter (optional parameters)
        variadic_param_obj = None
        if variadic_data := func_data.get("variadic_parameter"):
            cty_type_obj = variadic_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType for variadic parameter '{variadic_data.get('name')}' in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")

            variadic_param_obj = pb.Function.Parameter(
                name=variadic_data.get("name", "options"),
                type=type_bytes,
                description=variadic_data.get("description", "Optional parameters"),
                allow_null_value=variadic_data.get("allow_null", True),
                allow_unknown_values=True,
            )

        # Process return type
        return_value_obj = None
        if return_data := func_data.get("return"):
            cty_type_obj = return_data.get("cty_type")
            if cty_type_obj is None:
                logger.warning(
                    f"Missing CtyType (key 'cty_type') for return value in function '{func_name}'. Defaulting to CtyDynamic."
                )
                from pyvider.cty import CtyDynamic

                cty_type_obj = CtyDynamic()

            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)
        else:
            logger.warning(
                f"No explicit 'return' data or CtyType for function '{func_name}'. Defaulting return to CtyDynamic for Protobuf."
            )
            from pyvider.cty import CtyDynamic

            cty_type_obj = CtyDynamic()
            type_bytes = json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")
            return_value_obj = pb.Function.Return(type=type_bytes)

        constructor_kwargs = {
            "parameters": parameters,
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
        }

        if variadic_param_obj:
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        if return_value_obj:
            constructor_kwargs["return"] = return_value_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error(f"Error converting '{func_name}' to protobuf: {e}", exc_info=False)
        return None

x_dict_to_proto_function__mutmut_mutants : ClassVar[MutantDict] = {
'x_dict_to_proto_function__mutmut_1': x_dict_to_proto_function__mutmut_1, 
    'x_dict_to_proto_function__mutmut_2': x_dict_to_proto_function__mutmut_2, 
    'x_dict_to_proto_function__mutmut_3': x_dict_to_proto_function__mutmut_3, 
    'x_dict_to_proto_function__mutmut_4': x_dict_to_proto_function__mutmut_4, 
    'x_dict_to_proto_function__mutmut_5': x_dict_to_proto_function__mutmut_5, 
    'x_dict_to_proto_function__mutmut_6': x_dict_to_proto_function__mutmut_6, 
    'x_dict_to_proto_function__mutmut_7': x_dict_to_proto_function__mutmut_7, 
    'x_dict_to_proto_function__mutmut_8': x_dict_to_proto_function__mutmut_8, 
    'x_dict_to_proto_function__mutmut_9': x_dict_to_proto_function__mutmut_9, 
    'x_dict_to_proto_function__mutmut_10': x_dict_to_proto_function__mutmut_10, 
    'x_dict_to_proto_function__mutmut_11': x_dict_to_proto_function__mutmut_11, 
    'x_dict_to_proto_function__mutmut_12': x_dict_to_proto_function__mutmut_12, 
    'x_dict_to_proto_function__mutmut_13': x_dict_to_proto_function__mutmut_13, 
    'x_dict_to_proto_function__mutmut_14': x_dict_to_proto_function__mutmut_14, 
    'x_dict_to_proto_function__mutmut_15': x_dict_to_proto_function__mutmut_15, 
    'x_dict_to_proto_function__mutmut_16': x_dict_to_proto_function__mutmut_16, 
    'x_dict_to_proto_function__mutmut_17': x_dict_to_proto_function__mutmut_17, 
    'x_dict_to_proto_function__mutmut_18': x_dict_to_proto_function__mutmut_18, 
    'x_dict_to_proto_function__mutmut_19': x_dict_to_proto_function__mutmut_19, 
    'x_dict_to_proto_function__mutmut_20': x_dict_to_proto_function__mutmut_20, 
    'x_dict_to_proto_function__mutmut_21': x_dict_to_proto_function__mutmut_21, 
    'x_dict_to_proto_function__mutmut_22': x_dict_to_proto_function__mutmut_22, 
    'x_dict_to_proto_function__mutmut_23': x_dict_to_proto_function__mutmut_23, 
    'x_dict_to_proto_function__mutmut_24': x_dict_to_proto_function__mutmut_24, 
    'x_dict_to_proto_function__mutmut_25': x_dict_to_proto_function__mutmut_25, 
    'x_dict_to_proto_function__mutmut_26': x_dict_to_proto_function__mutmut_26, 
    'x_dict_to_proto_function__mutmut_27': x_dict_to_proto_function__mutmut_27, 
    'x_dict_to_proto_function__mutmut_28': x_dict_to_proto_function__mutmut_28, 
    'x_dict_to_proto_function__mutmut_29': x_dict_to_proto_function__mutmut_29, 
    'x_dict_to_proto_function__mutmut_30': x_dict_to_proto_function__mutmut_30, 
    'x_dict_to_proto_function__mutmut_31': x_dict_to_proto_function__mutmut_31, 
    'x_dict_to_proto_function__mutmut_32': x_dict_to_proto_function__mutmut_32, 
    'x_dict_to_proto_function__mutmut_33': x_dict_to_proto_function__mutmut_33, 
    'x_dict_to_proto_function__mutmut_34': x_dict_to_proto_function__mutmut_34, 
    'x_dict_to_proto_function__mutmut_35': x_dict_to_proto_function__mutmut_35, 
    'x_dict_to_proto_function__mutmut_36': x_dict_to_proto_function__mutmut_36, 
    'x_dict_to_proto_function__mutmut_37': x_dict_to_proto_function__mutmut_37, 
    'x_dict_to_proto_function__mutmut_38': x_dict_to_proto_function__mutmut_38, 
    'x_dict_to_proto_function__mutmut_39': x_dict_to_proto_function__mutmut_39, 
    'x_dict_to_proto_function__mutmut_40': x_dict_to_proto_function__mutmut_40, 
    'x_dict_to_proto_function__mutmut_41': x_dict_to_proto_function__mutmut_41, 
    'x_dict_to_proto_function__mutmut_42': x_dict_to_proto_function__mutmut_42, 
    'x_dict_to_proto_function__mutmut_43': x_dict_to_proto_function__mutmut_43, 
    'x_dict_to_proto_function__mutmut_44': x_dict_to_proto_function__mutmut_44, 
    'x_dict_to_proto_function__mutmut_45': x_dict_to_proto_function__mutmut_45, 
    'x_dict_to_proto_function__mutmut_46': x_dict_to_proto_function__mutmut_46, 
    'x_dict_to_proto_function__mutmut_47': x_dict_to_proto_function__mutmut_47, 
    'x_dict_to_proto_function__mutmut_48': x_dict_to_proto_function__mutmut_48, 
    'x_dict_to_proto_function__mutmut_49': x_dict_to_proto_function__mutmut_49, 
    'x_dict_to_proto_function__mutmut_50': x_dict_to_proto_function__mutmut_50, 
    'x_dict_to_proto_function__mutmut_51': x_dict_to_proto_function__mutmut_51, 
    'x_dict_to_proto_function__mutmut_52': x_dict_to_proto_function__mutmut_52, 
    'x_dict_to_proto_function__mutmut_53': x_dict_to_proto_function__mutmut_53, 
    'x_dict_to_proto_function__mutmut_54': x_dict_to_proto_function__mutmut_54, 
    'x_dict_to_proto_function__mutmut_55': x_dict_to_proto_function__mutmut_55, 
    'x_dict_to_proto_function__mutmut_56': x_dict_to_proto_function__mutmut_56, 
    'x_dict_to_proto_function__mutmut_57': x_dict_to_proto_function__mutmut_57, 
    'x_dict_to_proto_function__mutmut_58': x_dict_to_proto_function__mutmut_58, 
    'x_dict_to_proto_function__mutmut_59': x_dict_to_proto_function__mutmut_59, 
    'x_dict_to_proto_function__mutmut_60': x_dict_to_proto_function__mutmut_60, 
    'x_dict_to_proto_function__mutmut_61': x_dict_to_proto_function__mutmut_61, 
    'x_dict_to_proto_function__mutmut_62': x_dict_to_proto_function__mutmut_62, 
    'x_dict_to_proto_function__mutmut_63': x_dict_to_proto_function__mutmut_63, 
    'x_dict_to_proto_function__mutmut_64': x_dict_to_proto_function__mutmut_64, 
    'x_dict_to_proto_function__mutmut_65': x_dict_to_proto_function__mutmut_65, 
    'x_dict_to_proto_function__mutmut_66': x_dict_to_proto_function__mutmut_66, 
    'x_dict_to_proto_function__mutmut_67': x_dict_to_proto_function__mutmut_67, 
    'x_dict_to_proto_function__mutmut_68': x_dict_to_proto_function__mutmut_68, 
    'x_dict_to_proto_function__mutmut_69': x_dict_to_proto_function__mutmut_69, 
    'x_dict_to_proto_function__mutmut_70': x_dict_to_proto_function__mutmut_70, 
    'x_dict_to_proto_function__mutmut_71': x_dict_to_proto_function__mutmut_71, 
    'x_dict_to_proto_function__mutmut_72': x_dict_to_proto_function__mutmut_72, 
    'x_dict_to_proto_function__mutmut_73': x_dict_to_proto_function__mutmut_73, 
    'x_dict_to_proto_function__mutmut_74': x_dict_to_proto_function__mutmut_74, 
    'x_dict_to_proto_function__mutmut_75': x_dict_to_proto_function__mutmut_75, 
    'x_dict_to_proto_function__mutmut_76': x_dict_to_proto_function__mutmut_76, 
    'x_dict_to_proto_function__mutmut_77': x_dict_to_proto_function__mutmut_77, 
    'x_dict_to_proto_function__mutmut_78': x_dict_to_proto_function__mutmut_78, 
    'x_dict_to_proto_function__mutmut_79': x_dict_to_proto_function__mutmut_79, 
    'x_dict_to_proto_function__mutmut_80': x_dict_to_proto_function__mutmut_80, 
    'x_dict_to_proto_function__mutmut_81': x_dict_to_proto_function__mutmut_81, 
    'x_dict_to_proto_function__mutmut_82': x_dict_to_proto_function__mutmut_82, 
    'x_dict_to_proto_function__mutmut_83': x_dict_to_proto_function__mutmut_83, 
    'x_dict_to_proto_function__mutmut_84': x_dict_to_proto_function__mutmut_84, 
    'x_dict_to_proto_function__mutmut_85': x_dict_to_proto_function__mutmut_85, 
    'x_dict_to_proto_function__mutmut_86': x_dict_to_proto_function__mutmut_86, 
    'x_dict_to_proto_function__mutmut_87': x_dict_to_proto_function__mutmut_87, 
    'x_dict_to_proto_function__mutmut_88': x_dict_to_proto_function__mutmut_88, 
    'x_dict_to_proto_function__mutmut_89': x_dict_to_proto_function__mutmut_89, 
    'x_dict_to_proto_function__mutmut_90': x_dict_to_proto_function__mutmut_90, 
    'x_dict_to_proto_function__mutmut_91': x_dict_to_proto_function__mutmut_91, 
    'x_dict_to_proto_function__mutmut_92': x_dict_to_proto_function__mutmut_92, 
    'x_dict_to_proto_function__mutmut_93': x_dict_to_proto_function__mutmut_93, 
    'x_dict_to_proto_function__mutmut_94': x_dict_to_proto_function__mutmut_94, 
    'x_dict_to_proto_function__mutmut_95': x_dict_to_proto_function__mutmut_95, 
    'x_dict_to_proto_function__mutmut_96': x_dict_to_proto_function__mutmut_96, 
    'x_dict_to_proto_function__mutmut_97': x_dict_to_proto_function__mutmut_97, 
    'x_dict_to_proto_function__mutmut_98': x_dict_to_proto_function__mutmut_98, 
    'x_dict_to_proto_function__mutmut_99': x_dict_to_proto_function__mutmut_99, 
    'x_dict_to_proto_function__mutmut_100': x_dict_to_proto_function__mutmut_100, 
    'x_dict_to_proto_function__mutmut_101': x_dict_to_proto_function__mutmut_101, 
    'x_dict_to_proto_function__mutmut_102': x_dict_to_proto_function__mutmut_102, 
    'x_dict_to_proto_function__mutmut_103': x_dict_to_proto_function__mutmut_103, 
    'x_dict_to_proto_function__mutmut_104': x_dict_to_proto_function__mutmut_104, 
    'x_dict_to_proto_function__mutmut_105': x_dict_to_proto_function__mutmut_105, 
    'x_dict_to_proto_function__mutmut_106': x_dict_to_proto_function__mutmut_106, 
    'x_dict_to_proto_function__mutmut_107': x_dict_to_proto_function__mutmut_107, 
    'x_dict_to_proto_function__mutmut_108': x_dict_to_proto_function__mutmut_108, 
    'x_dict_to_proto_function__mutmut_109': x_dict_to_proto_function__mutmut_109, 
    'x_dict_to_proto_function__mutmut_110': x_dict_to_proto_function__mutmut_110, 
    'x_dict_to_proto_function__mutmut_111': x_dict_to_proto_function__mutmut_111, 
    'x_dict_to_proto_function__mutmut_112': x_dict_to_proto_function__mutmut_112, 
    'x_dict_to_proto_function__mutmut_113': x_dict_to_proto_function__mutmut_113, 
    'x_dict_to_proto_function__mutmut_114': x_dict_to_proto_function__mutmut_114, 
    'x_dict_to_proto_function__mutmut_115': x_dict_to_proto_function__mutmut_115, 
    'x_dict_to_proto_function__mutmut_116': x_dict_to_proto_function__mutmut_116, 
    'x_dict_to_proto_function__mutmut_117': x_dict_to_proto_function__mutmut_117, 
    'x_dict_to_proto_function__mutmut_118': x_dict_to_proto_function__mutmut_118, 
    'x_dict_to_proto_function__mutmut_119': x_dict_to_proto_function__mutmut_119, 
    'x_dict_to_proto_function__mutmut_120': x_dict_to_proto_function__mutmut_120, 
    'x_dict_to_proto_function__mutmut_121': x_dict_to_proto_function__mutmut_121, 
    'x_dict_to_proto_function__mutmut_122': x_dict_to_proto_function__mutmut_122, 
    'x_dict_to_proto_function__mutmut_123': x_dict_to_proto_function__mutmut_123, 
    'x_dict_to_proto_function__mutmut_124': x_dict_to_proto_function__mutmut_124, 
    'x_dict_to_proto_function__mutmut_125': x_dict_to_proto_function__mutmut_125, 
    'x_dict_to_proto_function__mutmut_126': x_dict_to_proto_function__mutmut_126, 
    'x_dict_to_proto_function__mutmut_127': x_dict_to_proto_function__mutmut_127, 
    'x_dict_to_proto_function__mutmut_128': x_dict_to_proto_function__mutmut_128, 
    'x_dict_to_proto_function__mutmut_129': x_dict_to_proto_function__mutmut_129, 
    'x_dict_to_proto_function__mutmut_130': x_dict_to_proto_function__mutmut_130, 
    'x_dict_to_proto_function__mutmut_131': x_dict_to_proto_function__mutmut_131, 
    'x_dict_to_proto_function__mutmut_132': x_dict_to_proto_function__mutmut_132, 
    'x_dict_to_proto_function__mutmut_133': x_dict_to_proto_function__mutmut_133, 
    'x_dict_to_proto_function__mutmut_134': x_dict_to_proto_function__mutmut_134, 
    'x_dict_to_proto_function__mutmut_135': x_dict_to_proto_function__mutmut_135, 
    'x_dict_to_proto_function__mutmut_136': x_dict_to_proto_function__mutmut_136, 
    'x_dict_to_proto_function__mutmut_137': x_dict_to_proto_function__mutmut_137, 
    'x_dict_to_proto_function__mutmut_138': x_dict_to_proto_function__mutmut_138, 
    'x_dict_to_proto_function__mutmut_139': x_dict_to_proto_function__mutmut_139, 
    'x_dict_to_proto_function__mutmut_140': x_dict_to_proto_function__mutmut_140, 
    'x_dict_to_proto_function__mutmut_141': x_dict_to_proto_function__mutmut_141, 
    'x_dict_to_proto_function__mutmut_142': x_dict_to_proto_function__mutmut_142, 
    'x_dict_to_proto_function__mutmut_143': x_dict_to_proto_function__mutmut_143, 
    'x_dict_to_proto_function__mutmut_144': x_dict_to_proto_function__mutmut_144, 
    'x_dict_to_proto_function__mutmut_145': x_dict_to_proto_function__mutmut_145, 
    'x_dict_to_proto_function__mutmut_146': x_dict_to_proto_function__mutmut_146, 
    'x_dict_to_proto_function__mutmut_147': x_dict_to_proto_function__mutmut_147, 
    'x_dict_to_proto_function__mutmut_148': x_dict_to_proto_function__mutmut_148, 
    'x_dict_to_proto_function__mutmut_149': x_dict_to_proto_function__mutmut_149, 
    'x_dict_to_proto_function__mutmut_150': x_dict_to_proto_function__mutmut_150, 
    'x_dict_to_proto_function__mutmut_151': x_dict_to_proto_function__mutmut_151, 
    'x_dict_to_proto_function__mutmut_152': x_dict_to_proto_function__mutmut_152, 
    'x_dict_to_proto_function__mutmut_153': x_dict_to_proto_function__mutmut_153, 
    'x_dict_to_proto_function__mutmut_154': x_dict_to_proto_function__mutmut_154, 
    'x_dict_to_proto_function__mutmut_155': x_dict_to_proto_function__mutmut_155, 
    'x_dict_to_proto_function__mutmut_156': x_dict_to_proto_function__mutmut_156, 
    'x_dict_to_proto_function__mutmut_157': x_dict_to_proto_function__mutmut_157, 
    'x_dict_to_proto_function__mutmut_158': x_dict_to_proto_function__mutmut_158, 
    'x_dict_to_proto_function__mutmut_159': x_dict_to_proto_function__mutmut_159, 
    'x_dict_to_proto_function__mutmut_160': x_dict_to_proto_function__mutmut_160, 
    'x_dict_to_proto_function__mutmut_161': x_dict_to_proto_function__mutmut_161, 
    'x_dict_to_proto_function__mutmut_162': x_dict_to_proto_function__mutmut_162, 
    'x_dict_to_proto_function__mutmut_163': x_dict_to_proto_function__mutmut_163, 
    'x_dict_to_proto_function__mutmut_164': x_dict_to_proto_function__mutmut_164, 
    'x_dict_to_proto_function__mutmut_165': x_dict_to_proto_function__mutmut_165, 
    'x_dict_to_proto_function__mutmut_166': x_dict_to_proto_function__mutmut_166, 
    'x_dict_to_proto_function__mutmut_167': x_dict_to_proto_function__mutmut_167, 
    'x_dict_to_proto_function__mutmut_168': x_dict_to_proto_function__mutmut_168, 
    'x_dict_to_proto_function__mutmut_169': x_dict_to_proto_function__mutmut_169, 
    'x_dict_to_proto_function__mutmut_170': x_dict_to_proto_function__mutmut_170, 
    'x_dict_to_proto_function__mutmut_171': x_dict_to_proto_function__mutmut_171, 
    'x_dict_to_proto_function__mutmut_172': x_dict_to_proto_function__mutmut_172, 
    'x_dict_to_proto_function__mutmut_173': x_dict_to_proto_function__mutmut_173, 
    'x_dict_to_proto_function__mutmut_174': x_dict_to_proto_function__mutmut_174, 
    'x_dict_to_proto_function__mutmut_175': x_dict_to_proto_function__mutmut_175, 
    'x_dict_to_proto_function__mutmut_176': x_dict_to_proto_function__mutmut_176, 
    'x_dict_to_proto_function__mutmut_177': x_dict_to_proto_function__mutmut_177, 
    'x_dict_to_proto_function__mutmut_178': x_dict_to_proto_function__mutmut_178, 
    'x_dict_to_proto_function__mutmut_179': x_dict_to_proto_function__mutmut_179, 
    'x_dict_to_proto_function__mutmut_180': x_dict_to_proto_function__mutmut_180, 
    'x_dict_to_proto_function__mutmut_181': x_dict_to_proto_function__mutmut_181, 
    'x_dict_to_proto_function__mutmut_182': x_dict_to_proto_function__mutmut_182, 
    'x_dict_to_proto_function__mutmut_183': x_dict_to_proto_function__mutmut_183, 
    'x_dict_to_proto_function__mutmut_184': x_dict_to_proto_function__mutmut_184, 
    'x_dict_to_proto_function__mutmut_185': x_dict_to_proto_function__mutmut_185, 
    'x_dict_to_proto_function__mutmut_186': x_dict_to_proto_function__mutmut_186, 
    'x_dict_to_proto_function__mutmut_187': x_dict_to_proto_function__mutmut_187, 
    'x_dict_to_proto_function__mutmut_188': x_dict_to_proto_function__mutmut_188, 
    'x_dict_to_proto_function__mutmut_189': x_dict_to_proto_function__mutmut_189, 
    'x_dict_to_proto_function__mutmut_190': x_dict_to_proto_function__mutmut_190, 
    'x_dict_to_proto_function__mutmut_191': x_dict_to_proto_function__mutmut_191
}

def dict_to_proto_function(*args, **kwargs):
    result = _mutmut_trampoline(x_dict_to_proto_function__mutmut_orig, x_dict_to_proto_function__mutmut_mutants, args, kwargs)
    return result 

dict_to_proto_function.__signature__ = _mutmut_signature(x_dict_to_proto_function__mutmut_orig)
x_dict_to_proto_function__mutmut_orig.__name__ = 'x_dict_to_proto_function'
