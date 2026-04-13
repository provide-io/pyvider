#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyDynamic, CtyType
from pyvider.cty.conversion import cty_to_native
import pyvider.protocols.tfprotov6.protobuf as pb


def simulate_unmarshal_and_convert(arg_proto: pb.DynamicValue, param_cty_type: "CtyType") -> Any:
    decoded_cty_val = unmarshal(arg_proto, schema=param_cty_type)
    native_arg = cty_to_native(decoded_cty_val)
    return native_arg


class TestFunctionArgumentConversion:
    def test_list_of_strings_conversion(self) -> None:
        native_list = ["Terraform", "100"]
        cty_val = CtyDynamic().validate(native_list)
        arg_proto = marshal(cty_val, schema=CtyDynamic())
        result = simulate_unmarshal_and_convert(arg_proto, CtyDynamic())
        assert result == ["Terraform", "100"]

    def test_list_of_numbers_conversion(self) -> None:
        native_list = [10, 20, 30.5]
        cty_val = CtyDynamic().validate(native_list)
        arg_proto = marshal(cty_val, schema=CtyDynamic())
        result = simulate_unmarshal_and_convert(arg_proto, CtyDynamic())
        assert result == [10, 20, 30.5]


# 🐍🏗️🔚
