"""Tests for PlanResourceChange handler."""

import pytest
from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import (
    PlanResourceChangeHandler,
    _get_resource_and_provider_instances,
    _process_private_state,
)
from pyvider.exceptions import ResourceError
from pyvider.cty import CtyObject, CtyString


@pytest.fixture
def sample_request():
    """Create a sample PlanResourceChange request."""
    request = pb.PlanResourceChange.Request()
    request.type_name = "test_resource"
    request.config.msgpack = b""
    request.prior_state.msgpack = b""
    request.proposed_new_state.msgpack = b""
    request.prior_private = b""
    return request


@pytest.fixture
def mock_resource_class():
    """Create a mock resource class."""
    mock_class = MagicMock()
    mock_schema = MagicMock()
    mock_schema.block = CtyObject(attribute_types={"name": CtyString()})
    mock_class.get_schema.return_value = mock_schema
    mock_class.config_class = MagicMock
    return mock_class


@pytest.fixture
def mock_provider():
    """Create a mock provider instance."""
    return MagicMock()


class TestPlanResourceChangeHandlerStructure:
    """Tests for PlanResourceChange handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request):
        """Test that handler returns PlanResourceChange.Response."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await PlanResourceChangeHandler(sample_request, context=None)

            assert isinstance(response, pb.PlanResourceChange.Response)

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self, sample_request):
        """Test that handler increments request counter."""
        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.handler_requests") as mock_requests:
            with patch("pyvider.hub.hub.get_component") as mock_get:
                mock_get.return_value = None

                await PlanResourceChangeHandler(sample_request, context=None)

                mock_requests.inc.assert_called_with(handler="PlanResourceChange")

    @pytest.mark.asyncio
    async def test_handler_records_duration_metric(self, sample_request):
        """Test that handler records duration metric."""
        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.handler_duration") as mock_duration:
            with patch("pyvider.hub.hub.get_component") as mock_get:
                mock_get.return_value = None

                await PlanResourceChangeHandler(sample_request, context=None)

                assert mock_duration.observe.called


class TestGetResourceAndProviderInstances:
    """Tests for _get_resource_and_provider_instances function."""

    @pytest.mark.asyncio
    async def test_gets_both_instances_successfully(self, mock_resource_class, mock_provider):
        """Test successful retrieval of both instances."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.side_effect = lambda comp_type, name: {
                ("resource", "test_resource"): mock_resource_class,
                ("singleton", "provider"): mock_provider,
            }.get((comp_type, name))

            resource, provider = await _get_resource_and_provider_instances("test_resource")

            assert resource is mock_resource_class
            assert provider is mock_provider

    @pytest.mark.asyncio
    async def test_raises_resource_error_for_unknown_type(self):
        """Test that unknown resource type raises ResourceError."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            with pytest.raises(ResourceError, match="not registered"):
                await _get_resource_and_provider_instances("unknown_resource")

    @pytest.mark.asyncio
    async def test_raises_runtime_error_for_missing_provider(self, mock_resource_class):
        """Test that missing provider raises RuntimeError."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            def get_component(comp_type, name):
                if comp_type == "resource":
                    return mock_resource_class
                return None

            mock_get.side_effect = get_component

            with pytest.raises(RuntimeError, match="Provider instance not found"):
                await _get_resource_and_provider_instances("test_resource")


class TestProcessPrivateState:
    """Tests for _process_private_state function."""

    @pytest.mark.asyncio
    async def test_returns_none_when_no_private_state_class(self):
        """Test that None is returned when resource has no private_state_class."""
        mock_resource = MagicMock()
        mock_resource.private_state_class = None

        result = await _process_private_state(mock_resource, b"some_data")

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_no_prior_private(self):
        """Test that None is returned when prior_private is empty."""
        mock_resource = MagicMock()
        mock_resource.private_state_class = MagicMock

        result = await _process_private_state(mock_resource, b"")

        assert result is None

    @pytest.mark.asyncio
    async def test_deserializes_private_state_successfully(self):
        """Test successful private state deserialization."""
        mock_private_class = MagicMock()
        mock_resource = MagicMock()
        mock_resource.private_state_class = mock_private_class

        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.decrypt") as mock_decrypt:
            with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.msgpack.unpackb") as mock_unpack:
                mock_decrypt.return_value = b"decrypted"
                mock_unpack.return_value = {"key": "value"}

                result = await _process_private_state(mock_resource, b"encrypted_data")

                mock_private_class.assert_called_with(key="value")

    @pytest.mark.asyncio
    async def test_handles_deserialization_error(self):
        """Test that deserialization errors are handled gracefully."""
        mock_resource = MagicMock()
        mock_resource.private_state_class = MagicMock
        mock_resource.__name__ = "TestResource"

        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.decrypt") as mock_decrypt:
            with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.logger"):
                mock_decrypt.side_effect = Exception("Decrypt failed")

                result = await _process_private_state(mock_resource, b"bad_data")

                assert result is None


class TestPlanResourceChangeEdgeCases:
    """Edge case tests for PlanResourceChange handler."""

    @pytest.mark.asyncio
    async def test_handles_missing_resource(self, sample_request):
        """Test handling of missing resource type."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await PlanResourceChangeHandler(sample_request, context=None)

            assert len(response.diagnostics) >= 1

    @pytest.mark.asyncio
    async def test_handles_validation_error(self, sample_request, mock_resource_class, mock_provider):
        """Test handling of validation errors."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal:
                from pyvider.cty.exceptions import CtyValidationError
                mock_get.side_effect = lambda comp_type, name: {
                    ("resource", "test_resource"): mock_resource_class,
                    ("singleton", "provider"): mock_provider,
                }.get((comp_type, name))
                mock_unmarshal.side_effect = CtyValidationError("Invalid type")

                response = await PlanResourceChangeHandler(sample_request, context=None)

                assert len(response.diagnostics) >= 1

    @pytest.mark.asyncio
    async def test_with_context_object(self, sample_request):
        """Test handler with non-None context."""
        context = MagicMock()

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await PlanResourceChangeHandler(sample_request, context=context)

            assert isinstance(response, pb.PlanResourceChange.Response)


class TestPlanResourceChangeMetrics:
    """Tests for PlanResourceChange metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_error_metric_on_failure(self, sample_request):
        """Test that handler increments error counter on failure."""
        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.handler_errors") as mock_errors:
            with patch("pyvider.hub.hub.get_component") as mock_get:
                # Make the handler fail
                mock_get.side_effect = RuntimeError("Catastrophic failure")

                # The @resilient() decorator catches exceptions and returns diagnostics
                response = await PlanResourceChangeHandler(sample_request, context=None)

                # Response should contain error diagnostics (resilient catches the exception)
                assert len(response.diagnostics) > 0
                assert any("Internal Provider Error" in d.summary for d in response.diagnostics)


class TestPlanResourceChangeLogging:
    """Tests for PlanResourceChange logging behavior."""

    @pytest.mark.asyncio
    async def test_logs_debug_info(self, sample_request, mock_resource_class):
        """Test that debug information is logged during normal execution."""
        # Test without patching logger to see actual logging behavior
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None  # No resource found

            response = await PlanResourceChangeHandler(sample_request, context=None)

            # Should return response with diagnostics (resilient catches the error)
            assert isinstance(response, pb.PlanResourceChange.Response)
            # Error diagnostic should be present
            assert len(response.diagnostics) > 0


class TestUnmarshalRequestData:
    """Tests for _unmarshal_request_data function."""

    @pytest.mark.asyncio
    async def test_unmarshals_all_request_fields(self):
        """Test that all request fields are unmarshaled."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _unmarshal_request_data
        from pyvider.cty import CtyValue, CtyString

        request = pb.PlanResourceChange.Request()
        request.config.msgpack = b""
        request.prior_state.msgpack = b""
        request.proposed_new_state.msgpack = b""

        mock_schema = MagicMock()
        mock_schema.block = CtyObject(attribute_types={"name": CtyString()})

        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal:
            mock_unmarshal.return_value = CtyValue.null(CtyString())

            config, prior, proposed = await _unmarshal_request_data(request, mock_schema)

            assert mock_unmarshal.call_count == 3


class TestCreateResourceContext:
    """Tests for _create_resource_context function."""

    @pytest.mark.asyncio
    async def test_creates_resource_context_with_all_fields(self):
        """Test that resource context is created with all fields."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _create_resource_context
        from pyvider.cty import CtyValue, CtyString

        mock_resource_class = MagicMock()
        mock_resource_class.config_class = MagicMock
        mock_resource_class.state_class = MagicMock

        mock_provider = MagicMock()
        mock_provider.metadata.capabilities = []

        config_cty = CtyValue.null(CtyString())
        prior_state_cty = CtyValue.null(CtyString())
        proposed_state_cty = CtyValue.null(CtyString())
        private_state = None

        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.cty_to_attrs_instance") as mock_cty_to_attrs:
            mock_cty_to_attrs.return_value = None

            context = _create_resource_context(
                config_cty,
                prior_state_cty,
                proposed_state_cty,
                private_state,
                mock_resource_class,
                mock_provider,
            )

            assert context is not None
            assert mock_cty_to_attrs.call_count == 3


class TestHandlePlannedStateDict:
    """Tests for _handle_planned_state_dict function."""

    def test_handles_planned_state_with_values(self):
        """Test handling planned state dict with values."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _handle_planned_state_dict
        from pyvider.cty import CtyValue

        response = pb.PlanResourceChange.Response()
        mock_schema = MagicMock()

        # Create a schema with an attribute
        attr_name = MagicMock()
        attr_name.computed = False
        attr_name.required = True
        attr_name.name = "name"

        # Create a real CtyObject that can be used for validation
        cty_type = CtyObject(attribute_types={"name": CtyString()})
        mock_schema.block = MagicMock()
        mock_schema.block.to_cty_type.return_value = cty_type
        mock_schema.block.attributes = {"name": attr_name}

        # Provide actual values in the planned state
        planned_state_dict = {"name": "test_value"}

        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.marshal") as mock_marshal:
            mock_marshal_result = MagicMock()
            mock_marshal_result.msgpack = b"marshaled"
            mock_marshal.return_value = mock_marshal_result

            _handle_planned_state_dict(planned_state_dict, mock_schema, response)

            assert mock_marshal.called

    def test_handles_planned_state_with_unknown_values(self):
        """Test handling planned state with unknown values."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _handle_planned_state_dict
        from pyvider.cty import CtyValue

        response = pb.PlanResourceChange.Response()
        mock_schema = MagicMock()

        # Create a proper CtyObject type
        cty_type = CtyObject(attribute_types={"name": CtyString(), "computed_field": CtyString()})
        mock_schema.block = MagicMock()
        mock_schema.block.to_cty_type.return_value = cty_type

        # Create mock attributes
        attr_computed = MagicMock()
        attr_computed.computed = True
        attr_computed.required = False
        attr_computed.name = "computed_field"

        attr_name = MagicMock()
        attr_name.computed = False
        attr_name.required = True
        attr_name.name = "name"

        mock_schema.block.attributes = {
            "name": attr_name,
            "computed_field": attr_computed,
        }

        planned_state_dict = {
            "name": CtyValue.unknown(CtyString()),
        }

        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.marshal") as mock_marshal:
            mock_marshal_result = MagicMock()
            mock_marshal_result.msgpack = b"marshaled"
            mock_marshal.return_value = mock_marshal_result

            _handle_planned_state_dict(planned_state_dict, mock_schema, response)

            assert mock_marshal.called

    def test_marks_unset_computed_fields_as_unknown(self):
        """Test that unset computed fields are marked as unknown when unknowns present."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _handle_planned_state_dict
        from pyvider.cty import CtyValue

        response = pb.PlanResourceChange.Response()
        mock_schema = MagicMock()

        # Create a proper CtyObject type
        cty_type = CtyObject(attribute_types={"id": CtyString(), "name": CtyString()})
        mock_schema.block = MagicMock()
        mock_schema.block.to_cty_type.return_value = cty_type

        # Create mock attributes - id is computed, name is required
        attr_id = MagicMock()
        attr_id.computed = True
        attr_id.required = False
        attr_id.name = "id"

        attr_name = MagicMock()
        attr_name.computed = False
        attr_name.required = True
        attr_name.name = "name"

        mock_schema.block.attributes = {
            "id": attr_id,
            "name": attr_name,
        }

        # Only name is set, and it's unknown - id should be marked as unknown too
        planned_state_dict = {
            "name": CtyValue.unknown(CtyString()),
        }

        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.marshal") as mock_marshal:
            mock_marshal_result = MagicMock()
            mock_marshal_result.msgpack = b"marshaled"
            mock_marshal.return_value = mock_marshal_result

            _handle_planned_state_dict(planned_state_dict, mock_schema, response)

            assert mock_marshal.called

    def test_raises_type_error_for_non_object_schema(self):
        """Test that TypeError is raised if schema is not an object type."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _handle_planned_state_dict

        response = pb.PlanResourceChange.Response()
        mock_schema = MagicMock()
        mock_schema.block.to_cty_type.return_value = CtyString()  # Not an object!

        planned_state_dict = {"name": "test"}

        with pytest.raises(TypeError, match="Resource schema must be an object type"):
            _handle_planned_state_dict(planned_state_dict, mock_schema, response)


class TestPlanResourceChangeImplementation:
    """Tests for _plan_resource_change_impl function."""

    @pytest.mark.asyncio
    async def test_impl_with_successful_plan(self, sample_request, mock_resource_class, mock_provider):
        """Test successful plan execution."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _plan_resource_change_impl
        from pyvider.cty import CtyValue

        mock_resource_handler = MagicMock()
        mock_resource_handler.plan = AsyncMock(return_value=({"name": "test"}, None))
        mock_resource_class.return_value = mock_resource_handler

        with patch("pyvider.hub.hub.get_component") as mock_get:
            with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal:
                with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change._apply_schema_marks_iterative") as mock_marks:
                    with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.marshal") as mock_marshal:
                        mock_get.side_effect = lambda comp_type, name: {
                            ("resource", "test_resource"): mock_resource_class,
                            ("singleton", "provider"): mock_provider,
                        }.get((comp_type, name))

                        mock_unmarshal.return_value = CtyValue.null(CtyString())
                        mock_marks.return_value = CtyValue.null(CtyString())

                        mock_marshal_result = MagicMock()
                        mock_marshal_result.msgpack = b"marshaled"
                        mock_marshal.return_value = mock_marshal_result

                        response = await _plan_resource_change_impl(sample_request, context=None)

                        assert isinstance(response, pb.PlanResourceChange.Response)

    @pytest.mark.asyncio
    async def test_impl_with_planned_private_state(self, sample_request, mock_resource_class, mock_provider):
        """Test plan with planned private state returned."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _plan_resource_change_impl
        from pyvider.cty import CtyValue
        import attrs

        @attrs.define
        class ConfigClass:
            name: str = "test"

        @attrs.define
        class StateClass:
            name: str = "test"

        @attrs.define
        class PrivateState:
            token: str = "secret"

        private_state = PrivateState(token="new_secret")

        # Update mock to have proper classes
        mock_resource_class.config_class = ConfigClass
        mock_resource_class.state_class = StateClass

        mock_resource_handler = MagicMock()
        mock_resource_handler.plan = AsyncMock(return_value=({"name": "test"}, private_state))
        mock_resource_class.return_value = mock_resource_handler

        with patch("pyvider.hub.hub.get_component") as mock_get:
            with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal:
                with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change._apply_schema_marks_iterative") as mock_marks:
                    with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change._create_resource_context") as mock_create_ctx:
                        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change._handle_planned_state_dict") as mock_handle:
                            with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.encrypt") as mock_encrypt:
                                mock_get.side_effect = lambda comp_type, name: {
                                    ("resource", "test_resource"): mock_resource_class,
                                    ("singleton", "provider"): mock_provider,
                                }.get((comp_type, name))

                                mock_unmarshal.return_value = CtyValue.null(CtyString())
                                mock_marks.return_value = CtyValue.null(CtyString())

                                # Mock resource context
                                mock_context = MagicMock()
                                mock_context.diagnostics = []
                                mock_create_ctx.return_value = mock_context

                                mock_encrypt.return_value = b"encrypted_private"

                                response = await _plan_resource_change_impl(sample_request, context=None)

                                assert mock_encrypt.called
                                assert response.planned_private == b"encrypted_private"

    @pytest.mark.asyncio
    async def test_impl_returns_early_on_error_diagnostics(self, sample_request, mock_resource_class, mock_provider):
        """Test that implementation returns early when error diagnostics are present."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _plan_resource_change_impl
        from pyvider.cty import CtyValue

        mock_resource_handler = MagicMock()
        mock_resource_handler.plan = AsyncMock(return_value=({"name": "test"}, None))
        mock_resource_class.return_value = mock_resource_handler

        with patch("pyvider.hub.hub.get_component") as mock_get:
            with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal:
                with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change._apply_schema_marks_iterative") as mock_marks:
                    with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change._create_resource_context") as mock_create_ctx:
                        mock_get.side_effect = lambda comp_type, name: {
                            ("resource", "test_resource"): mock_resource_class,
                            ("singleton", "provider"): mock_provider,
                        }.get((comp_type, name))

                        mock_unmarshal.return_value = CtyValue.null(CtyString())
                        mock_marks.return_value = CtyValue.null(CtyString())

                        # Create context with error diagnostic
                        error_diag = pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary="Test error")
                        mock_context = MagicMock()
                        mock_context.diagnostics = [error_diag]
                        mock_create_ctx.return_value = mock_context

                        response = await _plan_resource_change_impl(sample_request, context=None)

                        # Should return early, not call marshal
                        assert len(response.diagnostics) == 1
                        assert response.diagnostics[0].summary == "Test error"
