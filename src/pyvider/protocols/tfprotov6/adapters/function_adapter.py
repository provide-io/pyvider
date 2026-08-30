#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import json
from typing import Any

from provide.foundation import logger

# FIX: Import the type encoder from its new, correct location in pyvider.cty
from pyvider.cty.conversion.type_encoder import encode_cty_type_to_wire_json
import pyvider.protocols.tfprotov6.protobuf as pb


def _wire_type_bytes(cty_type_obj: Any) -> bytes:
    """Encode a cty type as the wire JSON tfplugin6 carries in an opaque bytes field."""
    return json.dumps(encode_cty_type_to_wire_json(cty_type_obj)).encode("utf-8")


def _declared_type_bytes(data: dict[str, Any], described: str, func_name: str) -> bytes:
    """The declared cty type for one parameter or return value, or dynamic if it declared none."""
    cty_type_obj = data.get("cty_type")
    if cty_type_obj is None:
        logger.warning(
            f"Missing CtyType (key 'cty_type') for {described} in function "
            f"'{func_name}'. Defaulting to CtyDynamic."
        )
        from pyvider.cty import CtyDynamic

        cty_type_obj = CtyDynamic()
    return _wire_type_bytes(cty_type_obj)


def _build_parameters(func_data: dict[str, Any], func_name: str) -> list[pb.Function.Parameter]:
    """The fixed parameters, in declaration order."""
    return [
        pb.Function.Parameter(
            name=param_data.get("name", ""),
            type=_declared_type_bytes(param_data, f"parameter '{param_data.get('name')}'", func_name),
            description=param_data.get("description", ""),
            allow_null_value=param_data.get("allow_null", False),
            allow_unknown_values=True,
        )
        for param_data in func_data.get("parameters", [])
    ]


def _build_variadic(func_data: dict[str, Any], func_name: str) -> pb.Function.Parameter | None:
    """The trailing variadic parameter, if the function declares one."""
    variadic_data = func_data.get("variadic_parameter")
    if not variadic_data:
        return None
    return pb.Function.Parameter(
        name=variadic_data.get("name", "options"),
        type=_declared_type_bytes(
            variadic_data, f"variadic parameter '{variadic_data.get('name')}'", func_name
        ),
        description=variadic_data.get("description", "Optional parameters"),
        allow_null_value=variadic_data.get("allow_null", True),
        allow_unknown_values=True,
    )


def _build_return(func_data: dict[str, Any], func_name: str) -> pb.Function.Return:
    """The return type. tfplugin6 requires one, so an undeclared return is dynamic."""
    return_data = func_data.get("return")
    if not return_data:
        logger.warning(
            f"No explicit 'return' data or CtyType for function '{func_name}'. "
            "Defaulting return to CtyDynamic for Protobuf."
        )
        from pyvider.cty import CtyDynamic

        return pb.Function.Return(type=_wire_type_bytes(CtyDynamic()))
    return pb.Function.Return(type=_declared_type_bytes(return_data, "return value", func_name))


def dict_to_proto_function(func_data: dict[str, Any]) -> pb.Function | None:
    """Converts a dictionary representation of a function to a Protobuf Function."""
    func_name = func_data.get("name", "unknown")
    try:
        constructor_kwargs: dict[str, Any] = {
            "parameters": _build_parameters(func_data, func_name),
            "summary": func_data.get("summary", ""),
            "description": func_data.get("description", ""),
            "deprecation_message": func_data.get("deprecation_message", ""),
            "return": _build_return(func_data, func_name),
        }

        if variadic_param_obj := _build_variadic(func_data, func_name):
            constructor_kwargs["variadic_parameter"] = variadic_param_obj

        return pb.Function(**constructor_kwargs)

    except Exception as e:
        logger.error("Error converting function to protobuf", func_name=func_name, error=str(e), exc_info=True)
        return None


# 🐍🏗️🔚
