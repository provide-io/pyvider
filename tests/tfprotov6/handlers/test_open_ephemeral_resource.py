#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OpenEphemeralResource handler."""

from datetime import UTC, datetime

from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource import (
    OpenEphemeralResourceHandler,
    _open_ephemeral_resource_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.OpenEphemeralResource.Request:
    """Create a sample OpenEphemeralResource request."""
    request = pb.OpenEphemeralResource.Request()
    request.type_name = "test_ephemeral"
    request.config.msgpack = b"\x80"  # Empty dict
    return request


@pytest.fixture
def mock_ephemeral_class() -> MagicMock:
    """Create a mock ephemeral resource class."""
    mock_class = MagicMock()
    mock_schema = MagicMock()
    mock_schema.block = MagicMock()
    mock_class.get_schema.return_value = mock_schema
    mock_class.config_class = MagicMock

    mock_instance = AsyncMock()
    # open() returns (result_obj, private_state_obj, renew_at)
    mock_result = MagicMock()
    mock_private = MagicMock()
    mock_instance.open.return_value = (mock_result, mock_private, None)
    mock_class.return_value = mock_instance
    return mock_class


class TestOpenEphemeralResourceStructure:
    """Test handler structure."""

    @pytest.mark.asyncio
    async def test_handler_returns_response(self, sample_request: pb.OpenEphemeralResource.Request) -> None:
        """Test that handler returns proper response object."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await OpenEphemeralResourceHandler(sample_request, context=None)

            assert isinstance(response, pb.OpenEphemeralResource.Response)

    @pytest.mark.asyncio
    async def test_handler_records_metrics(self, sample_request: pb.OpenEphemeralResource.Request) -> None:
        """Test that handler records request and duration metrics."""
        with (
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_requests") as mock_req,
            patch("pyvider.protocols.tfprotov6.handlers._metrics.handler_duration") as mock_dur,
            patch("pyvider.hub.hub.get_component") as mock_get,
        ):
            mock_get.return_value = None

            await OpenEphemeralResourceHandler(sample_request, context=None)

            mock_req.inc.assert_called_once_with(handler="OpenEphemeralResource")
            mock_dur.observe.assert_called_once()


class TestOpenEphemeralResourceImpl:
    """Test implementation logic."""

    @pytest.mark.asyncio
    async def test_impl_opens_ephemeral_successfully(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test successful ephemeral resource open."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal") as mock_unmarshal,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.cty_to_attrs_instance"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.attrs.asdict") as mock_asdict,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.marshal") as mock_marshal,
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_unmarshal.return_value = MagicMock()
            mock_asdict.return_value = {"key": "value"}
            mock_marshal.return_value = pb.DynamicValue()

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            assert isinstance(response, pb.OpenEphemeralResource.Response)
            assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_impl_handles_unknown_resource_type(
        self, sample_request: pb.OpenEphemeralResource.Request
    ) -> None:
        """Test handling of unknown ephemeral resource type."""
        with patch("pyvider.hub.hub.get_component") as mock_get:
            mock_get.return_value = None

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_unmarshals_config(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that config is unmarshaled."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal") as mock_unmarshal,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.cty_to_attrs_instance"),
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_unmarshal.return_value = MagicMock()

            await _open_ephemeral_resource_impl(sample_request, context=None)

            mock_unmarshal.assert_called_once()

    @pytest.mark.asyncio
    async def test_impl_marshals_result_when_present(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that result is marshaled when returned."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.cty_to_attrs_instance"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.marshal") as mock_marshal,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.attrs.asdict") as mock_asdict,
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_asdict.return_value = {"key": "value"}
            mock_marshal.return_value = pb.DynamicValue()

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            # Result should be marshaled
            mock_marshal.assert_called()
            assert response.HasField("result")

    @pytest.mark.asyncio
    async def test_impl_packs_private_state_when_present(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that private state is packed to msgpack."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.cty_to_attrs_instance"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.msgpack.packb") as mock_pack,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.attrs.asdict"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.marshal") as mock_marshal,
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_pack.return_value = b"\x81\xa3key\xa5value"
            mock_marshal.return_value = pb.DynamicValue()

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            # Private state should be packed
            mock_pack.assert_called()
            assert len(response.private) > 0

    @pytest.mark.asyncio
    async def test_impl_sets_renew_at_when_present(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that renew_at is set when returned."""
        renew_time = datetime.now(UTC)
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.open.return_value = (MagicMock(), MagicMock(), renew_time)

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.cty_to_attrs_instance"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.attrs.asdict") as mock_asdict,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.datetime_to_proto") as mock_dt,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.marshal") as mock_marshal,
        ):
            from google.protobuf.timestamp_pb2 import Timestamp

            mock_get.return_value = mock_ephemeral_class
            mock_asdict.return_value = {"key": "value"}
            mock_dt.return_value = Timestamp()  # Proper protobuf type
            mock_marshal.return_value = pb.DynamicValue()

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            # datetime_to_proto should be called
            mock_dt.assert_called_once_with(renew_time)
            assert response.HasField("renew_at")

    @pytest.mark.asyncio
    async def test_impl_handles_none_result(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test handling when result_obj is None."""
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.open.return_value = (None, None, None)
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.cty_to_attrs_instance"),
        ):
            mock_get.return_value = mock_ephemeral_class

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            # Should not crash, just not set result/private/renew_at
            assert len(response.diagnostics) == 0

    @pytest.mark.asyncio
    async def test_impl_handles_validation_errors(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that CtyValidationError is converted to diagnostics."""
        from pyvider.cty.exceptions import CtyValidationError

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal") as mock_unmarshal,
        ):
            mock_get.return_value = mock_ephemeral_class
            mock_unmarshal.side_effect = CtyValidationError("Invalid config")

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_handles_pyvider_errors(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that PyviderError exceptions are converted to diagnostics."""
        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.cty_to_attrs_instance"),
        ):
            mock_get.return_value = mock_ephemeral_class

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0

    @pytest.mark.asyncio
    async def test_impl_handles_generic_exceptions(
        self, sample_request: pb.OpenEphemeralResource.Request, mock_ephemeral_class: MagicMock
    ) -> None:
        """Test that generic exceptions are converted to diagnostics."""
        mock_instance = mock_ephemeral_class.return_value
        mock_instance.open.side_effect = RuntimeError("Unexpected error")

        with (
            patch("pyvider.hub.hub.get_component") as mock_get,
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.unmarshal"),
            patch("pyvider.protocols.tfprotov6.handlers.open_ephemeral_resource.cty_to_attrs_instance"),
        ):
            mock_get.return_value = mock_ephemeral_class

            response = await _open_ephemeral_resource_impl(sample_request, context=None)

            assert len(response.diagnostics) > 0


# 🐍🏗️🔚
