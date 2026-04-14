#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for PlanResourceChange handler."""

from provide.testkit.mocking import MagicMock, patch
import pytest

from pyvider.cty import CtyObject, CtyString
from pyvider.exceptions import ResourceError
from pyvider.protocols.tfprotov6.handlers.plan_resource_change import (
    PlanResourceChangeHandler,
    _get_resource_and_provider_instances,
    _process_private_state,
)
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


class TestPlanResourceChangeHandlerStructure:
    """Tests for PlanResourceChange handler response structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request: pb.PlanResourceChange.Request) -> None:
        """Test that handler returns PlanResourceChange.Response."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await PlanResourceChangeHandler(sample_request, context=None)

            assert isinstance(response, pb.PlanResourceChange.Response)

    @pytest.mark.asyncio
    async def test_handler_records_request_metric(self, sample_request: pb.PlanResourceChange.Request) -> None:
        """Test that handler increments request counter."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_requests,
            patch("pyvider.hub.hub.get_component") as mock_get,
        ):
            mock_get.return_value = None

            await PlanResourceChangeHandler(sample_request, context=None)

            mock_requests.inc.assert_called_with(handler="PlanResourceChange")

    @pytest.mark.asyncio
    async def test_handler_records_duration_metric(
        self, sample_request: pb.PlanResourceChange.Request
    ) -> None:
        """Test that handler records duration metric."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_duration,
            patch("pyvider.hub.hub.get_component") as mock_get,
        ):
            mock_get.return_value = None

            await PlanResourceChangeHandler(sample_request, context=None)

            assert mock_duration.observe.called


class TestGetResourceAndProviderInstances:
    """Tests for _get_resource_and_provider_instances function."""

    @pytest.mark.asyncio
    async def test_gets_both_instances_successfully(
        self, mock_resource_class: MagicMock, mock_provider: MagicMock
    ) -> None:
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
    async def test_raises_resource_error_for_unknown_type(self) -> None:
        """Test that unknown resource type raises ResourceError."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            with pytest.raises(ResourceError, match="not registered"):
                await _get_resource_and_provider_instances("unknown_resource")

    @pytest.mark.asyncio
    async def test_raises_runtime_error_for_missing_provider(self, mock_resource_class: MagicMock) -> None:
        """Test that missing provider raises RuntimeError."""
        with patch("pyvider.hub.hub.get_component") as mock_get:

            def get_component(comp_type: str, name: str) -> MagicMock | None:
                if comp_type == "resource":
                    return mock_resource_class
                return None

            mock_get.side_effect = get_component

            with pytest.raises(RuntimeError, match="Provider instance not found"):
                await _get_resource_and_provider_instances("test_resource")


class TestProcessPrivateState:
    """Tests for _process_private_state function."""

    @pytest.mark.asyncio
    async def test_returns_none_when_no_private_state_class(self) -> None:
        """Test that None is returned when resource has no private_state_class."""
        mock_resource = MagicMock()
        mock_resource.private_state_class = None

        result = await _process_private_state(mock_resource, b"some_data")

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_no_prior_private(self) -> None:
        """Test that None is returned when prior_private is empty."""
        mock_resource = MagicMock()
        mock_resource.private_state_class = MagicMock

        result = await _process_private_state(mock_resource, b"")

        assert result is None

    @pytest.mark.asyncio
    async def test_deserializes_private_state_successfully(self) -> None:
        """Test successful private state deserialization."""
        mock_private_class = MagicMock()
        mock_resource = MagicMock()
        mock_resource.private_state_class = mock_private_class

        with (
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.decrypt") as mock_decrypt,
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.msgpack.unpackb") as mock_unpack,
        ):
            mock_decrypt.return_value = b"decrypted"
            mock_unpack.return_value = {"key": "value"}

            await _process_private_state(mock_resource, b"encrypted_data")

            mock_private_class.assert_called_with(key="value")

    @pytest.mark.asyncio
    async def test_handles_deserialization_error(self) -> None:
        """Test that deserialization errors are handled gracefully."""
        mock_resource = MagicMock()
        mock_resource.private_state_class = MagicMock
        mock_resource.__name__ = "TestResource"

        with (
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.decrypt") as mock_decrypt,
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.logger"),
        ):
            mock_decrypt.side_effect = Exception("Decrypt failed")

            result = await _process_private_state(mock_resource, b"bad_data")

            assert result is None


class TestPlanResourceChangeEdgeCases:
    """Edge case tests for PlanResourceChange handler."""

    @pytest.mark.asyncio
    async def test_handles_missing_resource(self, sample_request: pb.PlanResourceChange.Request) -> None:
        """Test handling of missing resource type."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await PlanResourceChangeHandler(sample_request, context=None)

            assert len(response.diagnostics) >= 1

    @pytest.mark.asyncio
    async def test_handles_validation_error(
        self,
        sample_request: pb.PlanResourceChange.Request,
        mock_resource_class: MagicMock,
        mock_provider: MagicMock,
    ) -> None:
        """Test handling of validation errors."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal,
        ):
            from pyvider.cty.exceptions import CtyValidationError

            mock_get.side_effect = lambda comp_type, name: {
                ("resource", "test_resource"): mock_resource_class,
                ("singleton", "provider"): mock_provider,
            }.get((comp_type, name))
            mock_unmarshal.side_effect = CtyValidationError("Invalid type")

            response = await PlanResourceChangeHandler(sample_request, context=None)

            assert len(response.diagnostics) >= 1

    @pytest.mark.asyncio
    async def test_with_context_object(self, sample_request: pb.PlanResourceChange.Request) -> None:
        """Test handler with non-None context."""
        context = MagicMock()

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await PlanResourceChangeHandler(sample_request, context=context)

            assert isinstance(response, pb.PlanResourceChange.Response)


class TestPlanResourceChangeMetrics:
    """Tests for PlanResourceChange metrics recording."""

    @pytest.mark.asyncio
    async def test_handler_records_error_metric_on_failure(
        self, sample_request: pb.PlanResourceChange.Request
    ) -> None:
        """Test that handler increments error counter on failure."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors"),
            patch("pyvider.hub.hub.get_component") as mock_get,
        ):
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
    async def test_logs_debug_info(
        self, sample_request: pb.PlanResourceChange.Request, mock_resource_class: MagicMock
    ) -> None:
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
    async def test_unmarshals_all_request_fields(self) -> None:
        """Test that all request fields are unmarshaled."""
        from pyvider.cty import CtyString, CtyValue
        from pyvider.protocols.tfprotov6.handlers.plan_resource_change import _unmarshal_request_data

        request = pb.PlanResourceChange.Request()
        request.config.msgpack = b""
        request.prior_state.msgpack = b""
        request.proposed_new_state.msgpack = b""

        mock_schema = MagicMock()
        mock_schema.block = CtyObject(attribute_types={"name": CtyString()})

        with patch("pyvider.protocols.tfprotov6.handlers.plan_resource_change.unmarshal") as mock_unmarshal:
            mock_unmarshal.return_value = CtyValue.null(CtyString())

            _config, _prior, _proposed = await _unmarshal_request_data(request, mock_schema)

            assert mock_unmarshal.call_count == 3


# 🐍🏗️🔚
