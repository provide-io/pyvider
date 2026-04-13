#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for PlanResourceChange handler - Implementation and complex scenarios."""

from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.cty import CtyObject, CtyString
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.PlanResourceChange.Request:
    """Create a sample PlanResourceChange request."""
    request = pb.PlanResourceChange.Request()
    request.type_name = "test_resource"
    request.config.msgpack = b""
    request.prior_state.msgpack = b""
    request.proposed_new_state.msgpack = b""
    request.prior_private = b""
    return request


@pytest.fixture
def mock_resource_class() -> MagicMock:
    """Create a mock resource class."""
    mock_class = MagicMock()
    mock_schema = MagicMock()
    mock_schema.block = CtyObject(attribute_types={"name": CtyString()})
    mock_class.get_schema.return_value = mock_schema
    mock_class.config_class = MagicMock
    mock_class._is_test_only = False
    return mock_class


@pytest.fixture
def mock_provider() -> MagicMock:
    """Create a mock provider instance."""
    return MagicMock()


class TestCreateResourceContext:
    """Tests for _create_resource_context function."""

    @pytest.mark.asyncio
    async def test_creates_resource_context_with_all_fields(self) -> None:
        """Test that resource context is created with all fields."""
        from pyvider.cty import CtyString, CtyValue
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _create_resource_context

        mock_resource_class = MagicMock()
        mock_resource_class.config_class = MagicMock
        mock_resource_class.state_class = MagicMock

        mock_provider = MagicMock()
        mock_provider.metadata.capabilities = []

        config_cty = CtyValue.null(CtyString())
        prior_state_cty = CtyValue.null(CtyString())
        proposed_state_cty = CtyValue.null(CtyString())
        private_state = None

        with patch(
            "pyvider.protocols.tfprotov6.handlers.plan_resource_change.cty_to_attrs_instance"
        ) as mock_cty_to_attrs:
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

    def test_handles_planned_state_with_values(self) -> None:
        """Test handling planned state dict with values."""
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _handle_planned_state_dict

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

    def test_handles_planned_state_with_unknown_values(self) -> None:
        """Test handling planned state with unknown values."""
        from pyvider.cty import CtyValue
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _handle_planned_state_dict

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

    def test_marks_unset_computed_fields_as_unknown(self) -> None:
        """Test that unset computed fields are marked as unknown when unknowns present."""
        from pyvider.cty import CtyValue
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _handle_planned_state_dict

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

    def test_raises_type_error_for_non_object_schema(self) -> None:
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
    async def test_impl_with_successful_plan(
        self,
        sample_request: pb.PlanResourceChange.Request,
        mock_resource_class: MagicMock,
        mock_provider: MagicMock,
    ) -> None:
        """Test successful plan execution."""
        from pyvider.cty import CtyValue
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _plan_resource_change_impl

        mock_resource_handler = MagicMock()
        mock_resource_handler.plan = AsyncMock(return_value=({"name": "test"}, None))
        mock_resource_class.return_value = mock_resource_handler

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.plan_resource_change._apply_schema_marks_iterative"
            ) as mock_marks,
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.marshal") as mock_marshal,
        ):
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
    async def test_impl_with_planned_private_state(
        self,
        sample_request: pb.PlanResourceChange.Request,
        mock_resource_class: MagicMock,
        mock_provider: MagicMock,
    ) -> None:
        """Test plan with planned private state returned."""
        import attrs

        from pyvider.cty import CtyValue
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _plan_resource_change_impl

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

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.plan_resource_change._apply_schema_marks_iterative"
            ) as mock_marks,
            patch(
                "pyvider.protocols.tfprotov6.handlers.plan_resource_change._create_resource_context"
            ) as mock_create_ctx,
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change._handle_planned_state_dict"),
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.encrypt") as mock_encrypt,
        ):
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
    async def test_impl_returns_early_on_error_diagnostics(
        self,
        sample_request: pb.PlanResourceChange.Request,
        mock_resource_class: MagicMock,
        mock_provider: MagicMock,
    ) -> None:
        """Test that implementation returns early when error diagnostics are present."""
        from pyvider.cty import CtyValue
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _plan_resource_change_impl

        mock_resource_handler = MagicMock()
        mock_resource_handler.plan = AsyncMock(return_value=({"name": "test"}, None))
        mock_resource_class.return_value = mock_resource_handler

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal,
            patch(
                "pyvider.protocols.tfprotov6.handlers.plan_resource_change._apply_schema_marks_iterative"
            ) as mock_marks,
            patch(
                "pyvider.protocols.tfprotov6.handlers.plan_resource_change._create_resource_context"
            ) as mock_create_ctx,
        ):
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


# 🐍🏗️🔚
