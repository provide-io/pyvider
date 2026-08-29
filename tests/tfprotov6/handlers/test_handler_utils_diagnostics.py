#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for handlers/utils.py utility functions - Diagnostics and edge cases."""

import attrs
from provide.foundation.errors import FoundationError
from provide.testkit.mocking import patch
import pytest

from pyvider.cty import CtyList, CtyNumber, CtyObject, CtyString
from pyvider.cty.exceptions import (
    CtyStringValidationError,
    CtyValidationError,
)
from pyvider.cty.path import CtyPath, GetAttrStep
from pyvider.cty.values import CtyValue
from pyvider.exceptions import (
    DataSourceError,
    FunctionError,
    PyviderError,
    ResourceError,
    ResourceLifecycleContractError,
)
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
    is_valid_refinement,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestCreateDiagnosticFromException:
    """Tests for create_diagnostic_from_exception function."""

    @pytest.mark.asyncio
    async def test_cty_string_validation_error(self) -> None:
        """Test diagnostic from CtyStringValidationError."""
        exc = CtyStringValidationError(message="Invalid string", value=123)

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Invalid string" in diag.summary

    @pytest.mark.asyncio
    async def test_cty_validation_error_with_path(self) -> None:
        """Test diagnostic includes path from CTY error."""
        exc = CtyValidationError(message="Validation failed", path=CtyPath(steps=[GetAttrStep(name="config")]))

        diag = await create_diagnostic_from_exception(exc)

        assert diag.attribute is not None
        assert len(diag.attribute.steps) == 1

    @pytest.mark.asyncio
    async def test_foundation_error_with_context(self) -> None:
        """Test diagnostic from FoundationError with context."""
        exc = FoundationError("Test error")
        exc.context = {
            "terraform.summary": "Custom summary",
            "terraform.detail": "Custom detail",
            "extra": "Extra info",
        }

        diag = await create_diagnostic_from_exception(exc)

        assert "Custom summary" in diag.summary
        assert "Custom detail" in diag.detail

    @pytest.mark.asyncio
    async def test_resource_lifecycle_contract_error(self) -> None:
        """Test diagnostic from ResourceLifecycleContractError."""
        exc = ResourceLifecycleContractError("Contract violated")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Contract violated" in diag.detail

    @pytest.mark.asyncio
    async def test_function_error(self) -> None:
        """Test diagnostic from FunctionError."""
        exc = FunctionError("Function failed")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Function failed" in diag.detail

    @pytest.mark.asyncio
    async def test_resource_error(self) -> None:
        """Test diagnostic from ResourceError."""
        exc = ResourceError("Resource operation failed")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Resource operation failed" in diag.detail

    @pytest.mark.asyncio
    async def test_data_source_error(self) -> None:
        """Test diagnostic from DataSourceError."""
        exc = DataSourceError("Data source failed")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Data source failed" in diag.detail

    @pytest.mark.asyncio
    async def test_pyvider_error(self) -> None:
        """Test diagnostic from PyviderError."""
        exc = PyviderError("Framework error")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Framework error" in diag.detail

    @pytest.mark.asyncio
    async def test_generic_exception(self) -> None:
        """Test diagnostic from generic exception."""
        exc = ValueError("Unexpected error")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "bug in the provider" in diag.detail.lower()


class TestCtyToAttrsInstance:
    """Tests for cty_to_attrs_instance function."""

    def test_returns_none_when_attrs_cls_is_none(self) -> None:
        """Test that None attrs_cls returns None."""
        cty_val = CtyValue(vtype=CtyString(), value="test")
        result = cty_to_attrs_instance(cty_val, None)

        assert result is None

    def test_raises_error_when_not_a_class(self) -> None:
        """Test that non-class raises TypeError."""
        cty_val = CtyValue(vtype=CtyString(), value="test")

        with pytest.raises(TypeError, match="must be a class"):
            cty_to_attrs_instance(cty_val, "not_a_class")

    def test_calls_base_resource_from_cty(self) -> None:
        """Test that it delegates to BaseResource.from_cty."""

        @attrs.define
        class TestConfig:
            name: str

        cty_val = CtyValue(
            vtype=CtyObject(attribute_types={"name": CtyString()}),
            value={"name": CtyValue(vtype=CtyString(), value="test")},
        )

        # This will test the delegation path
        # The actual conversion is tested in BaseResource tests
        # We just verify no errors occur
        with patch("pyvider.protocols.tfprotov6.handlers.utils.BaseResource.from_cty") as mock_from_cty:
            mock_from_cty.return_value = TestConfig(name="test")

            result = cty_to_attrs_instance(cty_val, TestConfig)

            mock_from_cty.assert_called_once_with(cty_val, TestConfig, apply_defaults=False)
            assert result.name == "test"


class TestAttrsToDictCircularReferences:
    """Tests for circular reference handling in attrs_to_dict_for_cty."""

    def test_circular_ref_in_non_attrs_objects(self) -> None:
        """Test circular reference handling for non-attrs objects."""

        # Create a circular reference with a plain class (not attrs)
        class PlainNode:
            def __init__(self, value: int) -> None:
                self.value = value
                self.next = None

        node1 = PlainNode(1)
        node2 = PlainNode(2)
        node1.next = node2
        node2.next = node1  # Create circular reference

        # This should handle circular refs in non-attrs objects
        result = attrs_to_dict_for_cty([node1, node2])

        # Should return the objects as-is since they're not attrs, str, int, float, bool, or None
        assert isinstance(result, list)


class TestIsValidRefinementEdgeCases:
    """Additional tests for is_valid_refinement edge cases."""

    def test_object_with_mismatched_keys(self) -> None:
        """Test object refinement fails when types differ (detected as type mismatch)."""
        plan_type = CtyObject(attribute_types={"name": CtyString(), "age": CtyNumber()})
        result_type = CtyObject(attribute_types={"name": CtyString()})  # Missing 'age'

        plan = CtyValue(
            vtype=plan_type,
            value={
                "name": CtyValue(vtype=CtyString(), value="Alice"),
                "age": CtyValue(vtype=CtyNumber(), value=30),
            },
        )
        result = CtyValue(vtype=result_type, value={"name": CtyValue(vtype=CtyString(), value="Alice")})

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        # Different attributes means type mismatch
        assert "type mismatch" in reason.lower()

    def test_object_with_invalid_nested_refinement(self) -> None:
        """Test object refinement fails when nested attribute refinement fails."""
        obj_type = CtyObject(attribute_types={"nested": CtyObject(attribute_types={"val": CtyString()})})

        plan = CtyValue(
            vtype=obj_type,
            value={
                "nested": CtyValue(
                    vtype=CtyObject(attribute_types={"val": CtyString()}),
                    value={"val": CtyValue(vtype=CtyString(), value="known")},
                )
            },
        )
        result = CtyValue(
            vtype=obj_type,
            value={
                "nested": CtyValue(
                    vtype=CtyObject(attribute_types={"val": CtyString()}),
                    value={"val": CtyValue(vtype=CtyString(), value="changed")},
                )
            },
        )

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "nested" in reason.lower()

    def test_collection_with_mismatched_length(self) -> None:
        """Test collection refinement fails when lengths don't match."""
        list_type = CtyList(element_type=CtyString())

        plan = CtyValue(
            vtype=list_type,
            value=[
                CtyValue(vtype=CtyString(), value="a"),
                CtyValue(vtype=CtyString(), value="b"),
            ],
        )
        result = CtyValue(
            vtype=list_type,
            value=[CtyValue(vtype=CtyString(), value="a")],  # One fewer element
        )

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "length" in reason.lower()

    def test_collection_with_invalid_element_refinement(self) -> None:
        """Test collection refinement fails when element refinement fails."""
        list_type = CtyList(element_type=CtyString())

        plan = CtyValue(
            vtype=list_type,
            value=[
                CtyValue(vtype=CtyString(), value="known"),
                CtyValue(vtype=CtyString(), value="also_known"),
            ],
        )
        result = CtyValue(
            vtype=list_type,
            value=[
                CtyValue(vtype=CtyString(), value="known"),
                CtyValue(vtype=CtyString(), value="changed"),  # Changed value
            ],
        )

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "[1]" in reason

    def test_refinement_with_concrete_value_mismatch(self) -> None:
        """A mismatch is reported, and the values are NOT disclosed.

        This reason becomes a `tfplugin6.Diagnostic`, which Terraform prints to
        the console and writes to its logs, and that channel has no redaction.
        Interpolating the values means a refinement mismatch on a sensitive
        attribute publishes the secret in plaintext -- and a mismatch on any
        attribute publishes whatever it holds.

        This test previously required both values to appear in the message.
        """
        plan = CtyValue(vtype=CtyString(), value="original")
        result = CtyValue(vtype=CtyString(), value="modified")

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "value mismatch" in reason.lower()
        assert "original" not in reason
        assert "modified" not in reason

    def test_marks_alone_are_not_a_contract_violation(self) -> None:
        """A resource echoing a sensitive input back is a valid refinement.

        The inbound path marks config from the schema, so a resource that puts
        a sensitive attribute into its state returns a value equal to the plan
        in every respect except its marks. `CtyValue.__eq__` counts marks, so
        comparing directly failed the apply on exactly the resources that
        handle secrets.
        """
        from pyvider.cty import CtyMap
        from pyvider.cty.marks import CtyMark

        map_type = CtyMap(element_type=CtyString())
        plan = map_type.validate({"password": "hunter2"})
        result = map_type.validate({"password": CtyString().validate("hunter2").mark(CtyMark("sensitive"))})

        is_valid, reason = is_valid_refinement(plan, result)

        assert is_valid, reason
        assert "hunter2" not in reason


class TestCreateDiagnosticEdgeCases:
    """Additional tests for create_diagnostic_from_exception edge cases."""

    @pytest.mark.asyncio
    async def test_foundation_error_with_dict_context(self) -> None:
        """Test diagnostic from FoundationError with dict context."""
        context_dict = {
            "terraform.summary": "Custom Summary",
            "terraform.detail": "Custom Detail",
            "custom.field": "custom_value",
        }
        exc = FoundationError("Base error message", context=context_dict)

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Custom Summary" in diag.summary
        assert "Custom Detail" in diag.detail
        assert "custom.field: custom_value" in diag.detail


# 🐍🏗️🔚
