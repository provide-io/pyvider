#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for functions/base.py module."""

import attrs
import pytest

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyNumber, CtyString
from pyvider.functions.base import FunctionParameter, FunctionReturnType


class TestFunctionParameter:
    """Tests for FunctionParameter class."""

    def test_create_valid_parameter(self) -> None:
        """Test creating a valid function parameter."""
        param = FunctionParameter(
            name="test_param",
            type=CtyString(),
            description="A test parameter",
            allow_null=True,
            allow_unknown=False,
        )
        assert param.name == "test_param"
        assert isinstance(param.type, CtyString)
        assert param.description == "A test parameter"
        assert param.allow_null is True
        assert param.allow_unknown is False

    def test_parameter_with_defaults(self) -> None:
        """Test parameter with default values."""
        param = FunctionParameter(name="simple", type=CtyNumber())
        assert param.name == "simple"
        assert param.description == ""
        assert param.allow_null is False
        assert param.allow_unknown is False

    def test_parameter_with_different_types(self) -> None:
        """Test parameters with various CTY types."""
        string_param = FunctionParameter(name="str_param", type=CtyString())
        assert isinstance(string_param.type, CtyString)

        number_param = FunctionParameter(name="num_param", type=CtyNumber())
        assert isinstance(number_param.type, CtyNumber)

        bool_param = FunctionParameter(name="bool_param", type=CtyBool())
        assert isinstance(bool_param.type, CtyBool)

        list_param = FunctionParameter(name="list_param", type=CtyList(element_type=CtyString()))
        assert isinstance(list_param.type, CtyList)

    def test_invalid_parameter_name_empty(self) -> None:
        """Test that empty parameter name raises ValueError."""
        with pytest.raises(ValueError, match="Invalid parameter name"):
            FunctionParameter(name="", type=CtyString())

    def test_invalid_parameter_name_not_identifier(self) -> None:
        """Test that invalid identifier raises ValueError."""
        with pytest.raises(ValueError, match="Invalid parameter name"):
            FunctionParameter(name="123invalid", type=CtyString())

        with pytest.raises(ValueError, match="Invalid parameter name"):
            FunctionParameter(name="invalid-name", type=CtyString())

        with pytest.raises(ValueError, match="Invalid parameter name"):
            FunctionParameter(name="invalid name", type=CtyString())

    def test_invalid_parameter_type(self) -> None:
        """Test that non-CtyType raises TypeError."""
        with pytest.raises(TypeError, match="must be an instance of CtyType"):
            FunctionParameter(name="test", type="not_a_cty_type")  # type: ignore

        with pytest.raises(TypeError, match="must be an instance of CtyType"):
            FunctionParameter(name="test", type=123)  # type: ignore

    def test_parameter_frozen(self) -> None:
        """Test that FunctionParameter is immutable."""
        param = FunctionParameter(name="test", type=CtyString())
        with pytest.raises(attrs.exceptions.FrozenInstanceError):  # attrs frozen raises FrozenInstanceError
            param.name = "changed"  # type: ignore


class TestFunctionReturnType:
    """Tests for FunctionReturnType class."""

    def test_create_valid_return_type(self) -> None:
        """Test creating a valid return type."""
        ret_type = FunctionReturnType(type=CtyString())
        assert isinstance(ret_type.type, CtyString)

    def test_return_type_with_different_types(self) -> None:
        """Test return types with various CTY types."""
        string_ret = FunctionReturnType(type=CtyString())
        assert isinstance(string_ret.type, CtyString)

        number_ret = FunctionReturnType(type=CtyNumber())
        assert isinstance(number_ret.type, CtyNumber)

        bool_ret = FunctionReturnType(type=CtyBool())
        assert isinstance(bool_ret.type, CtyBool)

        dynamic_ret = FunctionReturnType(type=CtyDynamic())
        assert isinstance(dynamic_ret.type, CtyDynamic)

    def test_invalid_return_type(self) -> None:
        """Test that non-CtyType raises TypeError."""
        with pytest.raises(TypeError, match="must be an instance of CtyType"):
            FunctionReturnType(type="not_a_cty_type")  # type: ignore

        with pytest.raises(TypeError, match="must be an instance of CtyType"):
            FunctionReturnType(type=None)  # type: ignore

    def test_return_type_frozen(self) -> None:
        """Test that FunctionReturnType is immutable."""
        ret_type = FunctionReturnType(type=CtyString())
        with pytest.raises(attrs.exceptions.FrozenInstanceError):  # attrs frozen raises FrozenInstanceError
            ret_type.type = CtyNumber()  # type: ignore


class TestFunctionParameterEdgeCases:
    """Edge case tests for function parameters."""

    def test_parameter_name_with_underscores(self) -> None:
        """Test valid names with underscores."""
        param = FunctionParameter(name="valid_name", type=CtyString())
        assert param.name == "valid_name"

        param2 = FunctionParameter(name="_private", type=CtyString())
        assert param2.name == "_private"

    def test_parameter_allow_both_null_and_unknown(self) -> None:
        """Test parameter allowing both null and unknown."""
        param = FunctionParameter(
            name="flexible",
            type=CtyDynamic(),
            allow_null=True,
            allow_unknown=True,
        )
        assert param.allow_null is True
        assert param.allow_unknown is True

    def test_parameter_with_long_description(self) -> None:
        """Test parameter with long description."""
        long_desc = "This is a very long description " * 10
        param = FunctionParameter(
            name="documented",
            type=CtyString(),
            description=long_desc,
        )
        assert param.description == long_desc
        assert len(param.description) > 100


# 🐍🏗️🔚
