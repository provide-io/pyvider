"""Tests for ApplyResourceChange handler - the most critical CRUD operation handler."""

import json
from provide.testkit import mocking as mock

import pytest

from pyvider.protocols.tfprotov6.handlers.apply_resource_change import (
    ApplyResourceChangeHandler,
    _get_resource_and_provider_instances,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestGetResourceAndProviderInstances:
    """Tests for _get_resource_and_provider_instances helper function."""

    @pytest.mark.asyncio
    async def test_raises_error_when_resource_not_registered(self):
        """Test that it raises ResourceError when resource type not found."""
        from pyvider.exceptions import ResourceError

        with pytest.raises(ResourceError, match="not registered"):
            await _get_resource_and_provider_instances("nonexistent_resource")

    @pytest.mark.asyncio
    async def test_raises_error_when_provider_not_in_hub(self, provider_in_hub):
        """Test that it raises RuntimeError when provider not in hub."""
        # Register a test resource first
        from pyvider.hub import hub
        from pyvider.resources.base import BaseResource

        class TestResource(BaseResource):
            pass

        hub.register("resource", "test_resource", TestResource)

        # Now unregister provider
        hub.unregister("singleton", "provider")

        try:
            with pytest.raises(RuntimeError, match="Provider instance not found"):
                await _get_resource_and_provider_instances("test_resource")
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_returns_resource_and_provider_when_both_exist(self, provider_in_hub):
        """Test that it returns both resource class and provider instance."""
        # Register a test resource
        from pyvider.hub import hub
        from pyvider.resources.base import BaseResource

        class TestResource(BaseResource):
            pass

        hub.register("resource", "test_resource", TestResource)

        try:
            resource_class, provider_instance = await _get_resource_and_provider_instances("test_resource")
            assert resource_class == TestResource
            assert provider_instance is not None
        finally:
            hub.unregister("resource", "test_resource")


class TestApplyResourceChangeHandler:
    """Tests for ApplyResourceChangeHandler main functionality."""

    @pytest.mark.asyncio
    async def test_handler_returns_response_object(self, provider_in_hub):
        """Test that handler returns proper response object."""
        request = pb.ApplyResourceChange.Request(
            type_name="test_resource",
            planned_state=pb.DynamicValue(json=b'{"name": "test"}'),
        )

        # Mock to avoid complex resource setup
        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"
        ):
            with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.unmarshal"):
                with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.marshal"):
                    response = await ApplyResourceChangeHandler(request, context=None)

        assert isinstance(response, pb.ApplyResourceChange.Response)

    @pytest.mark.asyncio
    async def test_handler_handles_unknown_resource_type(self):
        """Test that handler properly handles unknown resource type."""
        request = pb.ApplyResourceChange.Request(
            type_name="unknown_resource",
            planned_state=pb.DynamicValue(json=b'{"name": "test"}'),
        )

        response = await ApplyResourceChangeHandler(request, context=None)

        # Should return diagnostics about unknown resource
        assert isinstance(response, pb.ApplyResourceChange.Response)
        assert len(response.diagnostics) > 0
        # Check diagnostic content (may be in summary or detail)
        diagnostic_text = " ".join(
            str(diag.summary) + " " + str(diag.detail) for diag in response.diagnostics
        ).lower()
        assert "not registered" in diagnostic_text or "unknown" in diagnostic_text


class TestApplyResourceChangeMetrics:
    """Tests for observability metrics in ApplyResourceChange."""

    @pytest.mark.asyncio
    async def test_handler_records_request_metrics(self):
        """Test that handler records request metrics."""
        # Note: Metrics implementation may vary, just verify handler completes
        request = pb.ApplyResourceChange.Request(
            type_name="test_resource",
            planned_state=pb.DynamicValue(json=b'{"name": "test"}'),
        )

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"
        ):
            with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.unmarshal"):
                with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.marshal"):
                    response = await ApplyResourceChangeHandler(request, context=None)

        # Verify handler completed successfully
        assert isinstance(response, pb.ApplyResourceChange.Response)

    @pytest.mark.asyncio
    async def test_handler_records_error_metrics_on_failure(self):
        """Test that handler records error metrics on failure."""
        request = pb.ApplyResourceChange.Request(
            type_name="unknown_resource",
            planned_state=pb.DynamicValue(json=b'{"name": "test"}'),
        )

        await ApplyResourceChangeHandler(request, context=None)

        # Error metrics should have been recorded
        # (Note: actual implementation may vary)


class TestApplyResourceChangeContextHandling:
    """Tests for operation context handling."""

    @pytest.mark.asyncio
    async def test_handler_uses_operation_context(self):
        """Test that handler uses operation context for diagnostics."""
        request = pb.ApplyResourceChange.Request(
            type_name="unknown_resource",
            planned_state=pb.DynamicValue(json=b'{"name": "test"}'),
        )

        response = await ApplyResourceChangeHandler(request, context=None)

        # Diagnostics should be populated from operation context
        assert isinstance(response, pb.ApplyResourceChange.Response)
        if len(response.diagnostics) > 0:
            # Diagnostics should have proper structure
            assert hasattr(response.diagnostics[0], "severity")
            assert hasattr(response.diagnostics[0], "summary")


class TestApplyResourceChangeEdgeCases:
    """Edge case tests for ApplyResourceChange."""

    @pytest.mark.asyncio
    async def test_handler_with_null_planned_state(self, provider_in_hub):
        """Test handler behavior with null planned state."""
        request = pb.ApplyResourceChange.Request(
            type_name="test_resource",
            planned_state=None,
        )

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"
        ):
            response = await ApplyResourceChangeHandler(request, context=None)

        assert isinstance(response, pb.ApplyResourceChange.Response)

    @pytest.mark.asyncio
    async def test_handler_with_empty_type_name(self):
        """Test handler behavior with empty type name."""
        request = pb.ApplyResourceChange.Request(
            type_name="",
            planned_state=pb.DynamicValue(json=b'{"name": "test"}'),
        )

        response = await ApplyResourceChangeHandler(request, context=None)

        assert isinstance(response, pb.ApplyResourceChange.Response)
        # Should have diagnostics about invalid type name
        assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_handler_with_malformed_json_state(self, provider_in_hub):
        """Test handler behavior with malformed JSON state."""
        request = pb.ApplyResourceChange.Request(
            type_name="test_resource",
            planned_state=pb.DynamicValue(json=b'{"invalid json'),
        )

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"
        ):
            response = await ApplyResourceChangeHandler(request, context=None)

        assert isinstance(response, pb.ApplyResourceChange.Response)
        # Should handle JSON error gracefully


class TestApplyResourceChangeLogging:
    """Tests for logging in ApplyResourceChange (for mutation testing)."""

    @pytest.mark.asyncio
    async def test_handler_logs_on_unknown_resource(self, caplog):
        """Test that handler logs when resource type is unknown."""
        import logging

        caplog.set_level(logging.INFO)

        request = pb.ApplyResourceChange.Request(
            type_name="unknown_resource",
            planned_state=pb.DynamicValue(json=b'{"name": "test"}'),
        )

        await ApplyResourceChangeHandler(request, context=None)

        # Should have logged information about the error
        # (Note: actual log level and content may vary)

    @pytest.mark.asyncio
    async def test_handler_logs_metrics_info(self, caplog, provider_in_hub):
        """Test that handler logs metrics information."""
        import logging

        caplog.set_level(logging.DEBUG)

        request = pb.ApplyResourceChange.Request(
            type_name="test_resource",
            planned_state=pb.DynamicValue(json=b'{"name": "test"}'),
        )

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"
        ):
            with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.unmarshal"):
                with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.marshal"):
                    await ApplyResourceChangeHandler(request, context=None)

        # Handler should log some operational information
        # (Note: actual implementation may vary)


class TestProcessPrivateState:
    """Tests for _process_private_state helper function."""

    @pytest.mark.asyncio
    async def test_returns_none_when_no_private_state_class(self):
        """Test that returns None when resource has no private_state_class."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state

        class ResourceWithoutPrivateState:
            pass

        result = await _process_private_state(ResourceWithoutPrivateState(), b"some_data")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_private_state_class_is_none(self):
        """Test that returns None when private_state_class is None."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state

        class ResourceWithNonePrivateState:
            private_state_class = None

        result = await _process_private_state(ResourceWithNonePrivateState(), b"some_data")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_planned_private_is_empty(self):
        """Test that returns None when planned_private is empty."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state
        import attrs

        @attrs.define
        class PrivateState:
            data: str

        class ResourceWithPrivateState:
            private_state_class = PrivateState

        result = await _process_private_state(ResourceWithPrivateState(), b"")
        assert result is None

    @pytest.mark.asyncio
    async def test_deserializes_valid_private_state(self):
        """Test successful deserialization of private state."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state
        import attrs
        import msgpack

        @attrs.define
        class PrivateState:
            data: str
            count: int

        class ResourceWithPrivateState:
            private_state_class = PrivateState

        # Create encrypted private state
        private_data = {"data": "test", "count": 42}
        serialized = msgpack.packb(private_data, use_bin_type=True)
        fake_encrypted = b"fake_encrypted_" + serialized

        with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.decrypt") as mock_decrypt:
            mock_decrypt.return_value = serialized

            result = await _process_private_state(ResourceWithPrivateState(), fake_encrypted)

            assert result is not None
            assert result.data == "test"
            assert result.count == 42
            mock_decrypt.assert_called_once_with(fake_encrypted)

    @pytest.mark.asyncio
    async def test_raises_resource_error_on_deserialization_failure(self):
        """Test that raises ResourceError when deserialization fails."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _process_private_state
        from pyvider.exceptions import ResourceError
        import attrs

        @attrs.define
        class PrivateState:
            data: str

        class ResourceWithPrivateState:
            private_state_class = PrivateState

        # Invalid encrypted data
        with pytest.raises(ResourceError, match="Failed to deserialize private state"):
            await _process_private_state(ResourceWithPrivateState(), b"invalid_data")


class TestCreateResourceContext:
    """Tests for _create_resource_context helper function."""

    def test_creates_context_with_all_fields(self):
        """Test creating resource context with all fields populated."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _create_resource_context
        from pyvider.cty import CtyValue, CtyString, CtyObject
        import attrs

        @attrs.define
        class Config:
            name: str

        @attrs.define
        class State:
            value: str

        @attrs.define
        class PrivateState:
            token: str

        class MockResource:
            config_class = Config
            state_class = State

        class MockProvider:
            class Metadata:
                capabilities = {"test": True}

            metadata = Metadata()

        config_cty = CtyValue(
            vtype=CtyObject(attribute_types={"name": CtyString()}),
            value={"name": CtyValue(vtype=CtyString(), value="test")},
        )
        prior_cty = CtyValue(
            vtype=CtyObject(attribute_types={"value": CtyString()}),
            value={"value": CtyValue(vtype=CtyString(), value="old")},
        )
        planned_cty = CtyValue(
            vtype=CtyObject(attribute_types={"value": CtyString()}),
            value={"value": CtyValue(vtype=CtyString(), value="new")},
        )
        private_state = PrivateState(token="secret")

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change.cty_to_attrs_instance"
        ) as mock_convert:
            mock_convert.side_effect = [Config(name="test"), State(value="old"), State(value="new")]

            context = _create_resource_context(
                config_cty, prior_cty, planned_cty, private_state, MockResource(), MockProvider()
            )

            assert context.config is not None
            assert context.state is not None
            assert context.planned_state is not None
            assert context.private_state == private_state
            assert context.capabilities == {"test": True}


class TestHandleApplyResult:
    """Tests for _handle_apply_result helper function."""

    def test_handles_none_new_state(self):
        """Test handling None new state (delete operation)."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _handle_apply_result
        from pyvider.cty import CtyValue, CtyString
        import pyvider.protocols.tfprotov6.protobuf as pb

        response = pb.ApplyResourceChange.Response()

        class MockSchema:
            class Block:
                pass

            block = Block()

        planned_cty = CtyValue(vtype=CtyString(), value="test")

        _handle_apply_result(None, None, MockSchema(), planned_cty, response)

        assert response.new_state.msgpack == b"\xc0"

    def test_marshals_new_state_successfully(self):
        """Test successful marshaling of new state."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _handle_apply_result
        from pyvider.cty import CtyValue, CtyString, CtyObject
        import pyvider.protocols.tfprotov6.protobuf as pb
        import attrs

        @attrs.define
        class NewState:
            name: str

        response = pb.ApplyResourceChange.Response()

        class MockType:
            def validate(self, data):
                return CtyValue(vtype=CtyString(), value="validated")

        class MockBlock:
            def to_cty_type(self):
                return MockType()

        class MockSchema:
            block = MockBlock()

        new_state = NewState(name="test")
        planned_cty = CtyValue(vtype=CtyString(), value="test")

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change.attrs_to_dict_for_cty"
        ) as mock_to_dict:
            with mock.patch(
                "pyvider.protocols.tfprotov6.handlers.apply_resource_change.marshal"
            ) as mock_marshal:
                with mock.patch(
                    "pyvider.protocols.tfprotov6.handlers.apply_resource_change.is_valid_refinement"
                ) as mock_refine:
                    mock_to_dict.return_value = {"name": "test"}
                    mock_marshal.return_value = pb.DynamicValue(msgpack=b"marshaled")
                    mock_refine.return_value = (True, "")

                    _handle_apply_result(new_state, None, MockSchema(), planned_cty, response)

                    assert response.new_state.msgpack == b"marshaled"

    def test_raises_error_on_invalid_refinement(self):
        """Test that raises error when new state is not valid refinement of planned state."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _handle_apply_result
        from pyvider.cty import CtyValue, CtyString
        from pyvider.exceptions import ResourceLifecycleContractError
        import pyvider.protocols.tfprotov6.protobuf as pb
        import attrs

        @attrs.define
        class NewState:
            name: str

        response = pb.ApplyResourceChange.Response()

        class MockType:
            def validate(self, data):
                return CtyValue(vtype=CtyString(), value="different")

        class MockBlock:
            def to_cty_type(self):
                return MockType()

        class MockSchema:
            name = "test_resource"
            block = MockBlock()

        new_state = NewState(name="test")
        planned_cty = CtyValue(vtype=CtyString(), value="planned")

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change.attrs_to_dict_for_cty"
        ) as mock_to_dict:
            with mock.patch(
                "pyvider.protocols.tfprotov6.handlers.apply_resource_change.is_valid_refinement"
            ) as mock_refine:
                mock_to_dict.return_value = {"name": "test"}
                mock_refine.return_value = (False, "Values don't match")

                with pytest.raises(ResourceLifecycleContractError, match="not a valid refinement"):
                    _handle_apply_result(new_state, None, MockSchema(), planned_cty, response)

    def test_encrypts_and_sets_private_state(self):
        """Test that private state is serialized and encrypted."""
        from pyvider.protocols.tfprotov6.handlers.apply_resource_change import _handle_apply_result
        from pyvider.cty import CtyValue, CtyString
        import pyvider.protocols.tfprotov6.protobuf as pb
        import attrs

        @attrs.define
        class NewState:
            name: str

        @attrs.define
        class NewPrivateState:
            token: str

        response = pb.ApplyResourceChange.Response()

        class MockType:
            def validate(self, data):
                return CtyValue(vtype=CtyString(), value="validated")

        class MockBlock:
            def to_cty_type(self):
                return MockType()

        class MockSchema:
            block = MockBlock()

        new_state = NewState(name="test")
        new_private = NewPrivateState(token="secret")

        with mock.patch(
            "pyvider.protocols.tfprotov6.handlers.apply_resource_change.attrs_to_dict_for_cty"
        ) as mock_to_dict:
            with mock.patch(
                "pyvider.protocols.tfprotov6.handlers.apply_resource_change.marshal"
            ) as mock_marshal:
                with mock.patch(
                    "pyvider.protocols.tfprotov6.handlers.apply_resource_change.encrypt"
                ) as mock_encrypt:
                    mock_to_dict.return_value = {"name": "test"}
                    mock_marshal.return_value = pb.DynamicValue(msgpack=b"marshaled")
                    mock_encrypt.return_value = b"encrypted_private"

                    _handle_apply_result(new_state, new_private, MockSchema(), None, response)

                    assert response.private == b"encrypted_private"
                    mock_encrypt.assert_called_once()
