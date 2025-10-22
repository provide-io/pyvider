"""Tests for handlers/utils.py utility functions."""

from unittest.mock import patch

import attrs
from provide.foundation.errors import FoundationError
import pytest

from pyvider.cty import CtyList, CtyNumber, CtyObject, CtyString
from pyvider.cty.exceptions import (
    CtyStringValidationError,
    CtyValidationError,
)
from pyvider.cty.path import CtyPath, GetAttrStep, IndexStep, KeyStep
from pyvider.cty.values import CtyValue
from pyvider.cty.values.markers import UNREFINED_UNKNOWN
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
    cty_path_to_proto_path,
    cty_to_attrs_instance,
    is_valid_refinement,
    str_path_to_proto_path,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestAttrsToDictForCty:
    """Tests for attrs_to_dict_for_cty function."""

    def test_converts_simple_attrs_instance(self):
        """Test converting simple attrs instance to dict."""

        @attrs.define
        class SimpleConfig:
            name: str
            count: int

        config = SimpleConfig(name="test", count=42)
        result = attrs_to_dict_for_cty(config)

        assert result == {"name": "test", "count": 42}

    def test_converts_nested_attrs_instances(self):
        """Test converting nested attrs instances."""

        @attrs.define
        class Inner:
            value: int

        @attrs.define
        class Outer:
            inner: Inner
            name: str

        config = Outer(inner=Inner(value=10), name="test")
        result = attrs_to_dict_for_cty(config)

        assert result == {"inner": {"value": 10}, "name": "test"}

    def test_preserves_tuples(self):
        """Test that tuples are preserved in conversion."""

        @attrs.define
        class Config:
            data: tuple

        config = Config(data=("a", "b", "c"))
        result = attrs_to_dict_for_cty(config)

        assert result == {"data": ("a", "b", "c")}
        assert isinstance(result["data"], tuple)

    def test_converts_lists(self):
        """Test that lists are converted recursively."""

        @attrs.define
        class Inner:
            val: int

        @attrs.define
        class Outer:
            items: list

        config = Outer(items=[Inner(val=1), Inner(val=2)])
        result = attrs_to_dict_for_cty(config)

        assert result == {"items": [{"val": 1}, {"val": 2}]}

    def test_converts_nested_dicts(self):
        """Test that nested dicts are converted."""

        @attrs.define
        class Inner:
            value: int

        @attrs.define
        class Outer:
            data: dict

        config = Outer(data={"key": Inner(value=5)})
        result = attrs_to_dict_for_cty(config)

        assert result == {"data": {"key": {"value": 5}}}

    def test_passes_through_primitives(self):
        """Test that primitives are passed through unchanged."""
        assert attrs_to_dict_for_cty("string") == "string"
        assert attrs_to_dict_for_cty(42) == 42
        assert attrs_to_dict_for_cty(3.14) == 3.14
        assert attrs_to_dict_for_cty(True) is True
        assert attrs_to_dict_for_cty(None) is None

    def test_passes_through_cty_values(self):
        """Test that CtyValue instances are passed through."""
        cty_val = CtyValue(vtype=CtyString(), value="test")
        result = attrs_to_dict_for_cty(cty_val)
        assert result is cty_val

    def test_handles_circular_references(self):
        """Test that circular references are detected."""

        @attrs.define
        class Node:
            name: str
            next: object = None

        # Create circular reference
        node1 = Node(name="first")
        node2 = Node(name="second", next=node1)
        node1.next = node2

        result = attrs_to_dict_for_cty(node1)

        # Should detect circular reference
        assert result["name"] == "first"
        assert "next" in result
        assert result["next"]["name"] == "second"
        # Circular ref should be marked
        assert "__circular_ref__" in result["next"]["next"]


class TestIsValidRefinement:
    """Tests for is_valid_refinement function."""

    def test_type_mismatch_returns_false(self):
        """Test that type mismatch is detected."""
        plan = CtyValue(vtype=CtyString(), value="test")
        result = CtyValue(vtype=CtyNumber(), value=42)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "Type mismatch" in reason

    def test_unknown_to_concrete_is_valid(self):
        """Test that unknown can be refined to concrete."""
        plan = CtyValue(vtype=CtyString(), value="test", is_unknown=True)
        result = CtyValue(vtype=CtyString(), value="concrete")

        is_valid, reason = is_valid_refinement(plan, result)

        assert is_valid
        assert reason == ""

    def test_unrefined_unknown_can_refine_to_any(self):
        """Test that UNREFINED_UNKNOWN can refine to any concrete value."""
        plan = CtyValue(vtype=CtyString(), value=UNREFINED_UNKNOWN, is_unknown=True)
        result = CtyValue(vtype=CtyString(), value="anything")

        is_valid, reason = is_valid_refinement(plan, result)

        assert is_valid

    def test_null_to_concrete_is_valid(self):
        """Test that null can be refined to concrete."""
        plan = CtyValue(vtype=CtyString(), value=None, is_null=True)
        result = CtyValue(vtype=CtyString(), value="concrete")

        is_valid, reason = is_valid_refinement(plan, result)

        assert is_valid

    def test_concrete_to_null_is_invalid(self):
        """Test that concrete cannot be refined to null."""
        plan = CtyValue(vtype=CtyString(), value="concrete")
        result = CtyValue(vtype=CtyString(), value=None, is_null=True)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "became null" in reason

    def test_known_to_unknown_is_invalid(self):
        """Test that known cannot become unknown."""
        plan = CtyValue(vtype=CtyString(), value="known")
        result = CtyValue(vtype=CtyString(), value="test", is_unknown=True)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "became unknown" in reason

    def test_concrete_value_change_is_invalid(self):
        """Test that concrete values cannot change."""
        plan = CtyValue(vtype=CtyString(), value="original")
        result = CtyValue(vtype=CtyString(), value="changed")

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "Value mismatch" in reason

    def test_object_refinement_key_mismatch(self):
        """Test object refinement detects key mismatches."""
        plan_obj = CtyValue(
            vtype=CtyObject(attribute_types={"a": CtyString()}),
            value={"a": CtyValue(vtype=CtyString(), value="test")},
        )
        result_obj = CtyValue(
            vtype=CtyObject(attribute_types={"b": CtyString()}),
            value={"b": CtyValue(vtype=CtyString(), value="test")},
        )

        is_valid, reason = is_valid_refinement(plan_obj, result_obj)

        assert not is_valid
        assert "attribute mismatch" in reason.lower() or "type mismatch" in reason.lower()

    def test_list_refinement_length_change(self):
        """Test list refinement detects length changes."""
        plan_list = CtyValue(
            vtype=CtyList(element_type=CtyString()), value=[CtyValue(vtype=CtyString(), value="a")]
        )
        result_list = CtyValue(
            vtype=CtyList(element_type=CtyString()),
            value=[CtyValue(vtype=CtyString(), value="a"), CtyValue(vtype=CtyString(), value="b")],
        )

        is_valid, reason = is_valid_refinement(plan_list, result_list)

        assert not is_valid
        assert "length changed" in reason.lower()


class TestStrPathToProtoPath:
    """Tests for str_path_to_proto_path function."""

    def test_simple_attribute_path(self):
        """Test converting simple attribute path."""
        result = str_path_to_proto_path("name")

        assert len(result.steps) == 1
        assert result.steps[0].attribute_name == "name"

    def test_nested_attribute_path(self):
        """Test converting nested attribute path."""
        result = str_path_to_proto_path("config.database.host")

        assert len(result.steps) == 3
        assert result.steps[0].attribute_name == "config"
        assert result.steps[1].attribute_name == "database"
        assert result.steps[2].attribute_name == "host"

    def test_index_path(self):
        """Test converting index path."""
        result = str_path_to_proto_path("items[0]")

        assert len(result.steps) == 2
        assert result.steps[0].attribute_name == "items"
        assert result.steps[1].element_key_int == 0

    def test_key_path(self):
        """Test converting key path."""
        result = str_path_to_proto_path("data['key']")

        assert len(result.steps) == 2
        assert result.steps[0].attribute_name == "data"
        assert result.steps[1].element_key_string == "key"

    def test_complex_nested_path(self):
        """Test converting complex nested path."""
        result = str_path_to_proto_path("config.servers[0].endpoints['primary']")

        assert len(result.steps) == 5
        assert result.steps[0].attribute_name == "config"
        assert result.steps[1].attribute_name == "servers"
        assert result.steps[2].element_key_int == 0
        assert result.steps[3].attribute_name == "endpoints"
        assert result.steps[4].element_key_string == "primary"

    def test_empty_path_returns_none(self):
        """Test that empty path returns None."""
        assert str_path_to_proto_path("") is None
        assert str_path_to_proto_path(None) is None


class TestCtyPathToProtoPath:
    """Tests for cty_path_to_proto_path function."""

    def test_getattr_step(self):
        """Test converting GetAttrStep."""
        cty_path = CtyPath(steps=[GetAttrStep(name="field")])
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 1
        assert result.steps[0].attribute_name == "field"

    def test_index_step(self):
        """Test converting IndexStep."""
        cty_path = CtyPath(steps=[IndexStep(index=5)])
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 1
        assert result.steps[0].element_key_int == 5

    def test_key_step(self):
        """Test converting KeyStep."""
        cty_path = CtyPath(steps=[KeyStep(key="mykey")])
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 1
        assert result.steps[0].element_key_string == "mykey"

    def test_mixed_steps(self):
        """Test converting mixed step types."""
        cty_path = CtyPath(
            steps=[
                GetAttrStep(name="root"),
                IndexStep(index=0),
                KeyStep(key="item"),
            ]
        )
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 3
        assert result.steps[0].attribute_name == "root"
        assert result.steps[1].element_key_int == 0
        assert result.steps[2].element_key_string == "item"

    def test_empty_path_returns_none(self):
        """Test that empty path returns None."""
        assert cty_path_to_proto_path(None) is None
        assert cty_path_to_proto_path(CtyPath(steps=[])) is None


class TestCreateDiagnosticFromException:
    """Tests for create_diagnostic_from_exception function."""

    @pytest.mark.asyncio
    async def test_cty_string_validation_error(self):
        """Test diagnostic from CtyStringValidationError."""
        exc = CtyStringValidationError(message="Invalid string", value=123)

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Invalid string" in diag.summary

    @pytest.mark.asyncio
    async def test_cty_validation_error_with_path(self):
        """Test diagnostic includes path from CTY error."""
        exc = CtyValidationError(message="Validation failed", path=CtyPath(steps=[GetAttrStep(name="config")]))

        diag = await create_diagnostic_from_exception(exc)

        assert diag.attribute is not None
        assert len(diag.attribute.steps) == 1

    @pytest.mark.asyncio
    async def test_foundation_error_with_context(self):
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
    async def test_resource_lifecycle_contract_error(self):
        """Test diagnostic from ResourceLifecycleContractError."""
        exc = ResourceLifecycleContractError("Contract violated")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Contract violated" in diag.detail

    @pytest.mark.asyncio
    async def test_function_error(self):
        """Test diagnostic from FunctionError."""
        exc = FunctionError("Function failed")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Function failed" in diag.detail

    @pytest.mark.asyncio
    async def test_resource_error(self):
        """Test diagnostic from ResourceError."""
        exc = ResourceError("Resource operation failed")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Resource operation failed" in diag.detail

    @pytest.mark.asyncio
    async def test_data_source_error(self):
        """Test diagnostic from DataSourceError."""
        exc = DataSourceError("Data source failed")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Data source failed" in diag.detail

    @pytest.mark.asyncio
    async def test_pyvider_error(self):
        """Test diagnostic from PyviderError."""
        exc = PyviderError("Framework error")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Framework error" in diag.detail

    @pytest.mark.asyncio
    async def test_generic_exception(self):
        """Test diagnostic from generic exception."""
        exc = ValueError("Unexpected error")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "bug in the provider" in diag.detail.lower()


class TestCtyToAttrsInstance:
    """Tests for cty_to_attrs_instance function."""

    def test_returns_none_when_attrs_cls_is_none(self):
        """Test that None attrs_cls returns None."""
        cty_val = CtyValue(vtype=CtyString(), value="test")
        result = cty_to_attrs_instance(cty_val, None)

        assert result is None

    def test_raises_error_when_not_a_class(self):
        """Test that non-class raises TypeError."""
        cty_val = CtyValue(vtype=CtyString(), value="test")

        with pytest.raises(TypeError, match="must be a class"):
            cty_to_attrs_instance(cty_val, "not_a_class")

    def test_calls_base_resource_from_cty(self):
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

            mock_from_cty.assert_called_once_with(cty_val, TestConfig)
            assert result.name == "test"


class TestAttrsToDictCircularReferences:
    """Tests for circular reference handling in attrs_to_dict_for_cty."""

    def test_circular_ref_in_non_attrs_objects(self):
        """Test circular reference handling for non-attrs objects."""
        # Create a circular reference with a plain class (not attrs)
        class PlainNode:
            def __init__(self, value):
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

    def test_object_with_mismatched_keys(self):
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
        result = CtyValue(
            vtype=result_type,
            value={"name": CtyValue(vtype=CtyString(), value="Alice")}
        )

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        # Different attributes means type mismatch
        assert "type mismatch" in reason.lower()

    def test_object_with_invalid_nested_refinement(self):
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

    def test_collection_with_mismatched_length(self):
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

    def test_collection_with_invalid_element_refinement(self):
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

    def test_refinement_with_concrete_value_mismatch(self):
        """Test refinement fails when concrete values don't match."""
        plan = CtyValue(vtype=CtyString(), value="original")
        result = CtyValue(vtype=CtyString(), value="modified")

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "value mismatch" in reason.lower()
        assert "original" in reason
        assert "modified" in reason


class TestCreateDiagnosticEdgeCases:
    """Additional tests for create_diagnostic_from_exception edge cases."""

    @pytest.mark.asyncio
    async def test_cty_validation_error_with_long_value(self):
        """Test diagnostic truncates very long value representations."""
        # Create a very long string value that should be truncated
        long_value = "x" * 200
        exc = CtyStringValidationError(
            "Value too long",
            value=long_value,
            type_name="string",
            path=CtyPath(steps=[GetAttrStep("test_field")]),
        )

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "..." in diag.detail  # Should be truncated

    @pytest.mark.asyncio
    async def test_cty_validation_error_without_value_attribute(self):
        """Test diagnostic handles validation errors without value attribute."""
        exc = CtyValidationError(
            "Generic validation failed",
            type_name="unknown",
            path=CtyPath(steps=[GetAttrStep("field")]),
        )
        # Ensure exc doesn't have 'value' attribute
        assert not hasattr(exc, "value")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "validation error" in diag.detail.lower()

    @pytest.mark.asyncio
    async def test_foundation_error_with_dict_context(self):
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

    @pytest.mark.asyncio
    async def test_foundation_error_with_non_dict_context(self):
        """Test diagnostic from FoundationError with non-dict context."""
        exc = FoundationError("Error message", context="string_context")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Error message" in diag.detail

    @pytest.mark.asyncio
    async def test_resource_lifecycle_contract_error_with_detail(self):
        """Test diagnostic from ResourceLifecycleContractError with detail attribute."""
        exc = ResourceLifecycleContractError("Contract violated")
        exc.detail = "Additional detail information"

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Contract violated" in diag.detail
        assert "Additional detail information" in diag.detail

    @pytest.mark.asyncio
    async def test_function_error_has_correct_summary(self):
        """Test FunctionError gets specific summary."""
        exc = FunctionError("Function execution failed", function_name="test_func")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Function Execution Error" in diag.summary

    @pytest.mark.asyncio
    async def test_resource_error_has_correct_summary(self):
        """Test ResourceError gets specific summary."""
        exc = ResourceError("Resource operation failed")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Provider Operation Error" in diag.summary

    @pytest.mark.asyncio
    async def test_data_source_error_has_correct_summary(self):
        """Test DataSourceError gets specific summary."""
        exc = DataSourceError("Data source read failed")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Provider Operation Error" in diag.summary

    @pytest.mark.asyncio
    async def test_pyvider_error_has_correct_summary(self):
        """Test PyviderError gets specific summary."""
        exc = PyviderError("Framework error occurred")

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Provider Framework Error" in diag.summary
