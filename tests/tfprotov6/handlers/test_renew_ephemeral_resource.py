#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for RenewEphemeralResource handler."""

from datetime import UTC, datetime

import msgpack
from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.exceptions import ResourceError
from pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource import (
    RenewEphemeralResourceHandler,
    _renew_ephemeral_resource_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.RenewEphemeralResource.Request:
    """Create a sample RenewEphemeralResource request."""
    private_data = {"token": "test_token", "resource_id": "res_123"}
    request = pb.RenewEphemeralResource.Request()
    request.type_name = "test_ephemeral"
    request.private = msgpack.packb(private_data)
    return request


@pytest.fixture
def mock_ephemeral_class() -> MagicMock:
    """Create a mock ephemeral resource class."""
    mock_class = MagicMock()
    mock_class.private_state_class = MagicMock
    mock_instance = AsyncMock()
    # renew() returns (new_private_state_obj, new_renew_at)
    mock_instance.renew.return_value = (MagicMock(), None)
    mock_class.return_value = mock_instance
    return mock_class


class TestRenewEphemeralResourceStructure:
    """Test handler structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request: pb.RenewEphemeralResource.Request) -> None:
        """Test that handler returns proper response object."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await RenewEphemeralResourceHandler(sample_request, context=None)

            assert isinstance(response, pb.RenewEphemeralResource.Response)

    @pytest.mark.asyncio
    async def test_handler_records_metrics(self, sample_request: pb.RenewEphemeralResource.Request) -> None:
        """Test that handler records request and duration metrics."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_req,
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_dur,
            patch("pyvider.hub.hub.get_component") as mock_get,
        ):
            mock_get.return_value = None

            await RenewEphemeralResourceHandler(sample_request, context=None)

            mock_req.inc.assert_called_once_with(handler="RenewEphemeralResource")
            mock_dur.observe.assert_called_once()


class TestRenewEphemeralResourceImpl:
    """Test implementation logic."""

    @pytest.mark.asyncio
    async def test_impl_renews_ephemeral_successfully(
        self, sample_request: pb.RenewEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test successful ephemeral resource renew."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.attrs.asdict") as mock_asdict,
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_asdict.return_value = {"token": "new_token"}

            response = await _renew_ephemeral_resource_impl(sample_request, context=None)

            assert isinstance(response, pb.RenewEphemeralResource.Response)
            assert len(response.diagnostics) == 0
            mock_ephemeral_class.return_value.renew.assert_called_once()

    @pytest.mark.asyncio
    async def test_impl_handles_unknown_resource_type(
        self, sample_request: pb.RenewEphemeralResource.Request
    ) -> None:
        """Test handling of unknown ephemeral resource type."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await _renew_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_handles_missing_private_state_class(
        self, sample_request: pb.RenewEphemeralResource.Request
    ) -> None:
        """Test handling when resource doesn't define private_state_class."""
        mock_class = MagicMock()
        mock_class.private_state_class = None

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = mock_class

            response = await _renew_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0
            assert "private_state_class" in response.diagnostics[0].detail

    @pytest.mark.asyncio
    async def test_impl_unpacks_private_data(
        self, sample_request: pb.RenewEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that private data is unpacked from msgpack."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch(
                "pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.msgpack.unpackb"
            ) as mock_unpack,
            patch("pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.attrs.asdict"),
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_unpack.return_value = {"token": "test_token"}

            await _renew_ephemeral_resource_impl(sample_request, context=None)

            mock_unpack.assert_called_once()

    @pytest.mark.asyncio
    async def test_impl_packs_new_private_state_when_present(
        self, sample_request: pb.RenewEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that new private state is packed to msgpack."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.msgpack.packb") as mock_pack,
            patch("pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.attrs.asdict") as mock_asdict,
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_asdict.return_value = {"token": "new_token"}
            mock_pack.return_value = b"\x81\xa5token\xa9new_token"

            response = await _renew_ephemeral_resource_impl(sample_request, context=None)

            mock_pack.assert_called()
            assert len(response.private) > 0

    @pytest.mark.asyncio
    async def test_impl_sets_renew_at_when_present(
        self, sample_request: pb.RenewEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that renew_at is set when returned."""
        from google.protobuf.timestamp_pb2 import Timestamp

        renew_time = datetime.now(UTC)
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.renew.return_value = (MagicMock(), renew_time)

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.attrs.asdict") as mock_asdict,
            patch("pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.msgpack.packb") as mock_pack,
            patch(
                "pyvider.protocols.tfprotov6.handlers.renew_ephemeral_resource.datetime_to_proto"
            ) as mock_dt,
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_asdict.return_value = {"token": "new_token"}
            mock_pack.return_value = b"\x81\xa5token\xa9new_token"
            mock_dt.return_value = Timestamp()

            response = await _renew_ephemeral_resource_impl(sample_request, context=None)

            mock_dt.assert_called_once_with(renew_time)
            assert response.HasField("renew_at")

    @pytest.mark.asyncio
    async def test_impl_handles_none_returns(
        self, sample_request: pb.RenewEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test handling when renew returns (None, None)."""
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.renew.return_value = (None, None)

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = mock_ephemeral_class

            response = await _renew_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_impl_handles_pyvider_errors(
        self, sample_request: pb.RenewEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that PyviderError exceptions are converted to diagnostics."""
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.renew.side_effect = ResourceError("Renew failed")

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = mock_ephemeral_class

            response = await _renew_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_handles_generic_exceptions(
        self, sample_request: pb.RenewEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that generic exceptions are converted to diagnostics."""
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.renew.side_effect = RuntimeError("Unexpected error")

        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = mock_ephemeral_class

            response = await _renew_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0


# 🐍🏗️🔚
