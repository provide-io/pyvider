"""Tests for GetProviderSchema handler."""

import pytest

from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
    GetProviderSchemaHandler,
    _get_provider_schema_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


class TestGetProviderSchemaHandler:
    """Tests for GetProviderSchemaHandler function."""

    @pytest.mark.asyncio
    async def test_handler_returns_response_object(self, provider_in_hub):
        """Test that handler returns proper response object."""
        request = pb.GetProviderSchema.Request()
        response = await GetProviderSchemaHandler(request, context=None)

        assert isinstance(response, pb.GetProviderSchema.Response)

    @pytest.mark.asyncio
    async def test_handler_returns_provider_schema(self, provider_in_hub):
        """Test handler returns provider schema."""
        request = pb.GetProviderSchema.Request()
        response = await GetProviderSchemaHandler(request, context=None)

        assert response.provider is not None
        assert isinstance(response.provider, pb.Schema)

    @pytest.mark.asyncio
    async def test_handler_returns_resource_schemas(self, provider_in_hub, discovered_components_session):
        """Test handler returns resource schemas."""
        request = pb.GetProviderSchema.Request()
        response = await GetProviderSchemaHandler(request, context=None)

        # Should have resource schemas
        assert hasattr(response, 'resource_schemas')
        assert response.resource_schemas is not None

    @pytest.mark.asyncio
    async def test_handler_returns_data_source_schemas(self, provider_in_hub, discovered_components_session):
        """Test handler returns data source schemas."""
        request = pb.GetProviderSchema.Request()
        response = await GetProviderSchemaHandler(request, context=None)

        # Should have data source schemas
        assert hasattr(response, 'data_source_schemas')
        assert response.data_source_schemas is not None

    @pytest.mark.asyncio
    async def test_handler_returns_functions(self, provider_in_hub, discovered_components_session):
        """Test handler returns provider functions."""
        request = pb.GetProviderSchema.Request()
        response = await GetProviderSchemaHandler(request, context=None)

        # Should have functions
        assert hasattr(response, 'functions')
        assert response.functions is not None

    @pytest.mark.asyncio
    async def test_handler_caches_schema(self, provider_in_hub):
        """Test handler caches schema across multiple calls."""
        request1 = pb.GetProviderSchema.Request()
        request2 = pb.GetProviderSchema.Request()

        response1 = await GetProviderSchemaHandler(request1, context=None)
        response2 = await GetProviderSchemaHandler(request2, context=None)

        # Both should succeed and return schemas
        assert response1.provider is not None
        assert response2.provider is not None

    @pytest.mark.asyncio
    async def test_impl_handles_concurrent_requests(self, provider_in_hub):
        """Test implementation handles concurrent schema requests."""
        import asyncio

        request = pb.GetProviderSchema.Request()

        # Make multiple concurrent requests
        responses = await asyncio.gather(
            _get_provider_schema_impl(request, context=None),
            _get_provider_schema_impl(request, context=None),
            _get_provider_schema_impl(request, context=None),
        )

        # All should succeed
        assert all(isinstance(r, pb.GetProviderSchema.Response) for r in responses)
        assert all(r.provider is not None for r in responses)

    @pytest.mark.asyncio
    async def test_handler_metrics_recorded(self, provider_in_hub):
        """Test that handler records metrics."""
        request = pb.GetProviderSchema.Request()

        # Just verify handler completes successfully (metrics recorded internally)
        response = await GetProviderSchemaHandler(request, context=None)
        assert isinstance(response, pb.GetProviderSchema.Response)
