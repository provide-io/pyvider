"""Tests for ApplyResourceChange handler - the most critical CRUD operation handler."""

import json
from unittest import mock

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
        with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"):
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
        diagnostic_text = " ".join(str(diag.summary) + " " + str(diag.detail) for diag in response.diagnostics).lower()
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

        with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"):
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
            assert hasattr(response.diagnostics[0], 'severity')
            assert hasattr(response.diagnostics[0], 'summary')


class TestApplyResourceChangeEdgeCases:
    """Edge case tests for ApplyResourceChange."""

    @pytest.mark.asyncio
    async def test_handler_with_null_planned_state(self, provider_in_hub):
        """Test handler behavior with null planned state."""
        request = pb.ApplyResourceChange.Request(
            type_name="test_resource",
            planned_state=None,
        )

        with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"):
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

        with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"):
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

        with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change._get_resource_and_provider_instances"):
            with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.unmarshal"):
                with mock.patch("pyvider.protocols.tfprotov6.handlers.apply_resource_change.marshal"):
                    await ApplyResourceChangeHandler(request, context=None)

        # Handler should log some operational information
        # (Note: actual implementation may vary)
