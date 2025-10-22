import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pyvider.protocols.service import ProtocolService
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def shutdown_event():
    return asyncio.Event()


def test_protocol_service_init(shutdown_event):
    service = ProtocolService(shutdown_event)
    assert isinstance(service._setup_complete, asyncio.Event)
    assert service._stream_active is True
    assert service._shutdown_event is shutdown_event
    assert isinstance(service._message_queue, asyncio.Queue)


@pytest.mark.asyncio
async def test_handle_shutdown(shutdown_event):
    service = ProtocolService(shutdown_event)
    await service._message_queue.put("message1")
    await service._message_queue.put("message2")

    await service.handle_shutdown()
    assert service._stream_active is False
    assert not service._message_queue.empty()

    await service._message_queue.put("message3")
    await service.handle_shutdown(force=True)
    assert service._stream_active is False
    assert service._message_queue.empty()


@pytest.mark.asyncio
async def test_start_stream_success(shutdown_event):
    service = ProtocolService(shutdown_event)
    service._setup_complete.set()
    context = MagicMock()
    response = await service.StartStream(MagicMock(), context)
    assert isinstance(response, pb.Empty)


@pytest.mark.asyncio
async def test_start_stream_timeout(shutdown_event):
    service = ProtocolService(shutdown_event)
    context = MagicMock()
    context.set_code = MagicMock()
    context.set_details = MagicMock()

    with pytest.raises(asyncio.TimeoutError):
        await service.StartStream(MagicMock(), context)

    context.set_code.assert_called_once_with("UNIMPLEMENTED")
    context.set_details.assert_called_once_with("Timeout waiting for StreamStdio setup")


@pytest.mark.asyncio
async def test_shutdown(shutdown_event):
    service = ProtocolService(shutdown_event)

    mock_shutdown_manager = MagicMock()
    mock_shutdown_manager.request_shutdown = MagicMock()
    mock_shutdown_manager.shutdown_tracers = AsyncMock()

    fake_server_module = MagicMock()
    fake_server_module.shutdown_manager = mock_shutdown_manager

    with patch.dict("sys.modules", {"pyvider.server": fake_server_module}):
        response = await service.Shutdown(MagicMock(), MagicMock())

        assert isinstance(response, pb.Empty)
        assert service._stream_active is False
        assert shutdown_event.is_set()
        mock_shutdown_manager.request_shutdown.assert_called_once()
        mock_shutdown_manager.shutdown_tracers.assert_awaited_once()


@pytest.mark.asyncio
async def test_stop_stream(shutdown_event):
    service = ProtocolService(shutdown_event)
    response = await service.StopStream(MagicMock(), MagicMock())
    assert isinstance(response, pb.Empty)
    assert service._stream_active is False


@pytest.mark.asyncio
async def test_stream_stdio_success(shutdown_event):
    service = ProtocolService(shutdown_event)

    async def mock_iterator():
        yield "message1"
        yield "message2"

    request_iterator = mock_iterator()

    responses = []
    async for response in service.StreamStdio(request_iterator, MagicMock()):
        responses.append(response)

    assert responses == ["message1", "message2"]
    assert service._message_queue.qsize() == 2
    assert service._setup_complete.is_set()
    assert service._stream_active is False
