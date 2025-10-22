"""Tests for handlers/utils.py utility functions."""

import pytest
import attrs
from unittest.mock import MagicMock

from pyvider.cty import CtyString, CtyNumber, CtyObject, CtyList, CtyTuple, CtyBool
from pyvider.cty.values import CtyValue
from pyvider.cty.values.markers import UNREFINED_UNKNOWN
from pyvider.cty.path import CtyPath, GetAttrStep, IndexStep, KeyStep
from pyvider.cty.exceptions import (
    CtyValidationError,
    CtyStringValidationError,
    CtyNumberValidationError,
    CtyListValidationError,
)
from pyvider.exceptions import (
    ResourceError,
    DataSourceError,
    FunctionError,
    ResourceLifecycleContractError,
    PyviderError,
)
from provide.foundation.errors import FoundationError
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.handlers.utils import (
    attrs_to_dict_for_cty,
    is_valid_refinement,
    str_path_to_proto_path,
    cty_path_to_proto_path,
    create_diagnostic_from_exception,
    cty_to_attrs_instance,
)


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
        cty_val = CtyValue(type=CtyString(), value="test")
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
        plan = CtyValue(type=CtyString(), value="test")
        result = CtyValue(type=CtyNumber(), value=42)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "Type mismatch" in reason

    def test_unknown_to_concrete_is_valid(self):
        """Test that unknown can be refined to concrete."""
        plan = CtyValue(type=CtyString(), value="test", unknown=True)
        result = CtyValue(type=CtyString(), value="concrete")

        is_valid, reason = is_valid_refinement(plan, result)

        assert is_valid
        assert reason == ""

    def test_unrefined_unknown_can_refine_to_any(self):
        """Test that UNREFINED_UNKNOWN can refine to any concrete value."""
        plan = CtyValue(type=CtyString(), value=UNREFINED_UNKNOWN)
        result = CtyValue(type=CtyString(), value="anything")

        is_valid, reason = is_valid_refinement(plan, result)

        assert is_valid

    def test_null_to_concrete_is_valid(self):
        """Test that null can be refined to concrete."""
        plan = CtyValue(type=CtyString(), value=None)
        result = CtyValue(type=CtyString(), value="concrete")

        is_valid, reason = is_valid_refinement(plan, result)

        assert is_valid

    def test_concrete_to_null_is_invalid(self):
        """Test that concrete cannot be refined to null."""
        plan = CtyValue(type=CtyString(), value="concrete")
        result = CtyValue(type=CtyString(), value=None)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "became null" in reason

    def test_known_to_unknown_is_invalid(self):
        """Test that known cannot become unknown."""
        plan = CtyValue(type=CtyString(), value="known")
        result = CtyValue(type=CtyString(), value="test", unknown=True)

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "became unknown" in reason

    def test_concrete_value_change_is_invalid(self):
        """Test that concrete values cannot change."""
        plan = CtyValue(type=CtyString(), value="original")
        result = CtyValue(type=CtyString(), value="changed")

        is_valid, reason = is_valid_refinement(plan, result)

        assert not is_valid
        assert "Value mismatch" in reason

    def test_object_refinement_key_mismatch(self):
        """Test object refinement detects key mismatches."""
        plan_obj = CtyValue(
            type=CtyObject(attribute_types={"a": CtyString()}),
            value={"a": CtyValue(type=CtyString(), value="test")}
        )
        result_obj = CtyValue(
            type=CtyObject(attribute_types={"b": CtyString()}),
            value={"b": CtyValue(type=CtyString(), value="test")}
        )

        is_valid, reason = is_valid_refinement(plan_obj, result_obj)

        assert not is_valid
        assert "attribute mismatch" in reason.lower()

    def test_list_refinement_length_change(self):
        """Test list refinement detects length changes."""
        plan_list = CtyValue(
            type=CtyList(element_type=CtyString()),
            value=[CtyValue(type=CtyString(), value="a")]
        )
        result_list = CtyValue(
            type=CtyList(element_type=CtyString()),
            value=[
                CtyValue(type=CtyString(), value="a"),
                CtyValue(type=CtyString(), value="b")
            ]
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

        assert len(result.steps) == 4
        assert result.steps[0].attribute_name == "config"
        assert result.steps[1].attribute_name == "servers"
        assert result.steps[2].element_key_int == 0
        assert result.steps[3].attribute_name == "endpoints"

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
        assert result.steps[1].element_key_int == 5

    def test_key_step(self):
        """Test converting KeyStep."""
        cty_path = CtyPath(steps=[KeyStep(key="mykey")])
        result = cty_path_to_proto_path(cty_path)

        assert len(result.steps) == 1
        assert result.steps[0].element_key_string == "mykey"

    def test_mixed_steps(self):
        """Test converting mixed step types."""
        cty_path = CtyPath(steps=[
            GetAttrStep(name="root"),
            IndexStep(index=0),
            KeyStep(key="item"),
        ])
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
        exc = CtyStringValidationError(
            message="Invalid string",
            type_name="string",
            value=123
        )

        diag = await create_diagnostic_from_exception(exc)

        assert diag.severity == pb.Diagnostic.ERROR
        assert "Invalid string" in diag.summary
        assert "string" in diag.detail

    @pytest.mark.asyncio
    async def test_cty_validation_error_with_path(self):
        """Test diagnostic includes path from CTY error."""
        exc = CtyValidationError(
            message="Validation failed",
            path=CtyPath(steps=[GetAttrStep(name="config")])
        )

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
            "extra": "Extra info"
        }

        diag = await create_diagnostic_from_exception(exc)

        assert "Custom summary" in diag.summary
        assert "Custom detail" in diag.detail

    @pytest.mark.asyncio
    async def test_resource_lifecycle_contract_error(self):
        """Test diagnostic from ResourceLifecycleContractError."""
        exc = ResourceLifecycleContractError("Contract violated")
        exc.detail = "Additional details"

        diag = await create_diagnostic_from_exception(exc)

        assert "Lifecycle Contract" in diag.summary
        assert "Contract violated" in diag.detail
        assert "Additional details" in diag.detail

    @pytest.mark.asyncio
    async def test_function_error(self):
        """Test diagnostic from FunctionError."""
        exc = FunctionError("Function failed")

        diag = await create_diagnostic_from_exception(exc)

        assert "Function Execution Error" in diag.summary
        assert "Function failed" in diag.detail

    @pytest.mark.asyncio
    async def test_resource_error(self):
        """Test diagnostic from ResourceError."""
        exc = ResourceError("Resource operation failed")

        diag = await create_diagnostic_from_exception(exc)

        assert "Provider Operation Error" in diag.summary
        assert "Resource operation failed" in diag.detail

    @pytest.mark.asyncio
    async def test_data_source_error(self):
        """Test diagnostic from DataSourceError."""
        exc = DataSourceError("Data source failed")

        diag = await create_diagnostic_from_exception(exc)

        assert "Provider Operation Error" in diag.summary
        assert "Data source failed" in diag.detail

    @pytest.mark.asyncio
    async def test_pyvider_error(self):
        """Test diagnostic from PyviderError."""
        exc = PyviderError("Framework error")

        diag = await create_diagnostic_from_exception(exc)

        assert "Provider Framework Error" in diag.summary
        assert "Framework error" in diag.detail

    @pytest.mark.asyncio
    async def test_generic_exception(self):
        """Test diagnostic from generic exception."""
        with pytest.mock.patch("pyvider.protocols.tfprotov6.handlers.utils.logger"):
            exc = ValueError("Unexpected error")

            diag = await create_diagnostic_from_exception(exc)

            assert "Internal Provider Error" in diag.summary
            assert "bug in the provider" in diag.detail.lower()


class TestCtyToAttrsInstance:
    """Tests for cty_to_attrs_instance function."""

    def test_returns_none_when_attrs_cls_is_none(self):
        """Test that None attrs_cls returns None."""
        cty_val = CtyValue(type=CtyString(), value="test")
        result = cty_to_attrs_instance(cty_val, None)

        assert result is None

    def test_raises_error_when_not_a_class(self):
        """Test that non-class raises TypeError."""
        cty_val = CtyValue(type=CtyString(), value="test")

        with pytest.raises(TypeError, match="must be a class"):
            cty_to_attrs_instance(cty_val, "not_a_class")

    def test_calls_base_resource_from_cty(self):
        """Test that it delegates to BaseResource.from_cty."""
        @attrs.define
        class TestConfig:
            name: str

        cty_val = CtyValue(
            type=CtyObject(attribute_types={"name": CtyString()}),
            value={"name": CtyValue(type=CtyString(), value="test")}
        )

        # This will test the delegation path
        # The actual conversion is tested in BaseResource tests
        # We just verify no errors occur
        with pytest.mock.patch("pyvider.protocols.tfprotov6.handlers.utils.BaseResource.from_cty") as mock_from_cty:
            mock_from_cty.return_value = TestConfig(name="test")

            result = cty_to_attrs_instance(cty_val, TestConfig)

            mock_from_cty.assert_called_once_with(cty_val, TestConfig)
            assert result.name == "test"
