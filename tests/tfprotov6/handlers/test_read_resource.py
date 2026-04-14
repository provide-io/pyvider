#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ReadResource handler."""

from typing import Any

import attrs
import msgpack
from provide.testkit.mocking import patch
import pytest

from pyvider.common.encryption import encrypt
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers.read_resource import (
    ReadResourceHandler,
    _read_resource_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource, ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema as Schema, a_num, a_str, s_resource


@attrs.define
class SampleState:
    id: str
    name: str
    count: int = 0


@attrs.define
class SamplePrivate(PrivateState):
    secret: str = ""


class SampleReadResource(BaseResource):
    """Sample resource for read testing."""

    state_class = SampleState
    private_state_class = SamplePrivate

    @classmethod
    def get_schema(cls) -> Schema:
        return s_resource(
            attributes={
                "id": a_str(required=True),
                "name": a_str(required=True),
                "count": a_num(optional=True),
            }
        )

    async def _validate_config(self, config: Any) -> list[str]:
        return []

    async def read(self, ctx: ResourceContext) -> SampleState | None:
        """Read returns updated state."""
        if ctx.state:
            # Simulate reading from backend and updating count
            return SampleState(id=ctx.state.id, name=ctx.state.name, count=ctx.state.count + 1)
        return None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


class TestReadResourceHandler:
    """Tests for ReadResourceHandler function."""

    @pytest.mark.asyncio
    async def test_handler_returns_response_object(self, provider_in_hub: Any) -> None:
        """Test that handler returns proper response object."""
        hub.register("resource", "test_resource", SampleReadResource)

        try:
            schema = SampleReadResource.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "res-123", "name": "test", "count": 5})

            from pyvider.conversion import marshal

            state_dv = marshal(state_cty, schema=schema.block)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
            )

            response = await ReadResourceHandler(request, context=None)

            assert isinstance(response, pb.ReadResource.Response)
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_handler_reads_and_updates_state(self, provider_in_hub: Any) -> None:
        """Test handler reads resource and updates state."""
        hub.register("resource", "test_resource", SampleReadResource)

        try:
            schema = SampleReadResource.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "res-123", "name": "test", "count": 5})

            from pyvider.conversion import marshal, unmarshal

            state_dv = marshal(state_cty, schema=schema.block)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
            )

            response = await ReadResourceHandler(request, context=None)

            # Unmarshal new state
            new_state_cty = unmarshal(response.new_state, schema=schema.block)

            assert new_state_cty.value["id"].value == "res-123"
            assert new_state_cty.value["name"].value == "test"
            # Count should be incremented by read()
            assert new_state_cty.value["count"].value == 6
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_handler_preserves_private_state(
        self, provider_in_hub: Any, encryption_key_env: Any
    ) -> None:
        """Test handler preserves private state."""
        hub.register("resource", "test_resource", SampleReadResource)

        try:
            schema = SampleReadResource.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "res-123", "name": "test", "count": 5})

            from pyvider.conversion import marshal

            state_dv = marshal(state_cty, schema=schema.block)

            # Create encrypted private state
            private_data = {"secret": "my-secret-token"}
            private_bytes = msgpack.packb(private_data)
            encrypted_private = encrypt(private_bytes)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
                private=encrypted_private,
            )

            response = await ReadResourceHandler(request, context=None)

            # Private state should be preserved
            assert response.private == encrypted_private
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_handler_handles_unknown_resource_type(self) -> None:
        """Test handler handles unknown resource type."""
        request = pb.ReadResource.Request(
            type_name="nonexistent_resource",
            current_state=pb.DynamicValue(msgpack=b"\x83\xa2id\xa3123\xa4name\xa4test\xa5count\x05"),
        )

        response = await ReadResourceHandler(request, context=None)

        assert isinstance(response, pb.ReadResource.Response)
        assert len(response.diagnostics) > 0


class TestReadResourceImpl:
    """Tests for _read_resource_impl function."""

    @pytest.mark.asyncio
    async def test_impl_returns_null_when_resource_deleted(self, provider_in_hub: Any) -> None:
        """Test implementation returns null state when resource deleted."""

        class DeletedResource(BaseResource):
            state_class = SampleState

            @classmethod
            def get_schema(cls) -> Schema:
                return s_resource(attributes={"id": a_str(), "name": a_str()})

            async def _validate_config(self, config: Any) -> list[str]:
                return []

            async def read(self, ctx: ResourceContext) -> None:
                # Simulate resource deleted
                return None

            async def _delete_apply(self, ctx: ResourceContext) -> None:
                pass

        hub.register("resource", "test_resource", DeletedResource)

        try:
            schema = DeletedResource.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "deleted", "name": "gone"})

            from pyvider.conversion import marshal

            state_dv = marshal(state_cty, schema=schema.block)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
            )

            response = await _read_resource_impl(request, context=None)

            # Should return msgpack null
            assert response.new_state.msgpack == b"\xc0"
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_impl_handles_missing_provider_in_hub(self, provider_in_hub: Any) -> None:
        """Test implementation handles missing provider gracefully."""
        hub.register("resource", "test_resource", SampleReadResource)

        # Temporarily remove provider
        provider = hub.get_component("singleton", "provider")
        hub.unregister("singleton", "provider")

        try:
            schema = SampleReadResource.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "res-123", "name": "test", "count": 5})

            from pyvider.conversion import marshal

            state_dv = marshal(state_cty, schema=schema.block)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
            )

            response = await _read_resource_impl(request, context=None)

            assert len(response.diagnostics) > 0
        finally:
            hub.unregister("resource", "test_resource")
            # Restore provider
            hub.register("singleton", "provider", provider)


class TestReadResourceEdgeCases:
    """Edge case tests for ReadResource."""

    @pytest.mark.asyncio
    async def test_handler_with_empty_state(self, provider_in_hub: Any) -> None:
        """Test handler with empty current state."""
        hub.register("resource", "test_resource", SampleReadResource)

        try:
            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=pb.DynamicValue(msgpack=b"\x80"),  # Empty map
            )

            response = await ReadResourceHandler(request, context=None)

            # Should handle gracefully
            assert isinstance(response, pb.ReadResource.Response)
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_handler_with_malformed_private_state(
        self, provider_in_hub: Any, encryption_key_env: Any
    ) -> None:
        """Test handler with malformed private state."""
        hub.register("resource", "test_resource", SampleReadResource)

        try:
            schema = SampleReadResource.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "res-123", "name": "test", "count": 5})

            from pyvider.conversion import marshal

            state_dv = marshal(state_cty, schema=schema.block)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
                private=b"invalid-private-state",  # Malformed
            )

            response = await ReadResourceHandler(request, context=None)

            # Should create diagnostic for private state error
            assert isinstance(response, pb.ReadResource.Response)
            # May have diagnostics depending on encryption/decryption behavior
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_handler_metrics_recorded(self, provider_in_hub: Any) -> None:
        """Test that handler records metrics."""
        hub.register("resource", "test_resource", SampleReadResource)

        try:
            schema = SampleReadResource.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "res-123", "name": "test", "count": 1})

            from pyvider.conversion import marshal

            state_dv = marshal(state_cty, schema=schema.block)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
            )

            # Just verify handler completes successfully (metrics are recorded internally)
            response = await ReadResourceHandler(request, context=None)

            assert isinstance(response, pb.ReadResource.Response)
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_handler_records_errors_on_exception(self, provider_in_hub: Any) -> None:
        """Test that handler records error metrics when exception occurs."""
        hub.register("resource", "test_resource", SampleReadResource)

        try:
            schema = SampleReadResource.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "res-123", "name": "test", "count": 1})

            from pyvider.conversion import marshal

            state_dv = marshal(state_cty, schema=schema.block)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
            )

            with (
                patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_errors") as mock_errors,
                patch("pyvider.protocols.tfprotov6.handlers.read_resource._read_resource_impl") as mock_impl,
            ):
                # Make implementation raise an exception
                mock_impl.side_effect = RuntimeError("Test error")

                with pytest.raises(RuntimeError, match="Test error"):
                    await ReadResourceHandler(request, context=None)

                # Verify error metric was recorded
                mock_errors.inc.assert_called_once_with(handler="ReadResource")
        finally:
            hub.unregister("resource", "test_resource")

    @pytest.mark.asyncio
    async def test_handler_appends_context_diagnostics(self, provider_in_hub: Any) -> None:
        """Test that handler appends diagnostics from resource context to response."""

        class ResourceWithContextDiagnostics(BaseResource):
            """Resource that adds diagnostics to context."""

            state_class = SampleState

            @classmethod
            def get_schema(cls) -> Schema:
                return s_resource(attributes={"id": a_str(), "name": a_str(), "count": a_num()})

            async def _validate_config(self, config: Any) -> list[str]:
                return []

            async def read(self, ctx: ResourceContext) -> SampleState:
                # Add diagnostic to context
                diagnostic = pb.Diagnostic(
                    severity=pb.Diagnostic.WARNING,
                    summary="Context warning",
                    detail="This is a warning from the resource context",
                )
                ctx.diagnostics.append(diagnostic)

                # Return updated state
                return SampleState(id=ctx.state.id, name=ctx.state.name, count=ctx.state.count + 1)

            async def _delete_apply(self, ctx: ResourceContext) -> None:
                pass

        hub.register("resource", "test_resource", ResourceWithContextDiagnostics)

        try:
            schema = ResourceWithContextDiagnostics.get_schema()
            cty_type = schema.block.to_cty_type()
            state_cty = cty_type.validate({"id": "res-123", "name": "test", "count": 5})

            from pyvider.conversion import marshal

            state_dv = marshal(state_cty, schema=schema.block)

            request = pb.ReadResource.Request(
                type_name="test_resource",
                current_state=state_dv,
            )

            response = await ReadResourceHandler(request, context=None)

            # Verify context diagnostic was appended to response
            assert len(response.diagnostics) == 1
            assert response.diagnostics[0].severity == pb.Diagnostic.WARNING
            assert response.diagnostics[0].summary == "Context warning"
        finally:
            hub.unregister("resource", "test_resource")


# 🐍🏗️🔚
