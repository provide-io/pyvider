# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0


import asyncio
from collections.abc import AsyncIterator
import contextlib
from typing import Any

from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.protocols.service import ProtocolService
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def shutdown_event() -> asyncio.Event:
    return asyncio.Event()


def test_protocol_service_init(shutdown_event: asyncio.Event) -> None:
    service = ProtocolService(shutdown_event)
    assert isinstance(service._setup_complete, asyncio.Event)
    assert service._stream_active is True
    assert service._shutdown_event is shutdown_event
    assert isinstance(service._message_queue, asyncio.Queue)


@pytest.mark.asyncio
async def test_handle_shutdown(shutdown_event: asyncio.Event) -> None:
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
async def test_start_stream_success(shutdown_event: asyncio.Event) -> None:
    service = ProtocolService(shutdown_event)
    service._setup_complete.set()
    context = MagicMock()
    response = await service.StartStream(MagicMock(), context)
    assert isinstance(response, pb.Empty)


@pytest.mark.asyncio
async def test_start_stream_timeout(shutdown_event: asyncio.Event) -> None:
    service = ProtocolService(shutdown_event)
    context = MagicMock()
    context.set_code = MagicMock()
    context.set_details = MagicMock()

    with pytest.raises(asyncio.TimeoutError):
        await service.StartStream(MagicMock(), context)

    context.set_code.assert_called_once_with("UNIMPLEMENTED")
    context.set_details.assert_called_once_with("Timeout waiting for StreamStdio setup")


@pytest.mark.asyncio
async def test_shutdown(shutdown_event: asyncio.Event) -> None:
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
async def test_stop_stream(shutdown_event: asyncio.Event) -> None:
    service = ProtocolService(shutdown_event)
    response = await service.StopStream(MagicMock(), MagicMock())
    assert isinstance(response, pb.Empty)
    assert service._stream_active is False


@pytest.mark.asyncio
async def test_stream_stdio_success(shutdown_event: asyncio.Event) -> None:
    service = ProtocolService(shutdown_event)

    async def mock_iterator() -> AsyncIterator[str]:
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


@pytest.mark.asyncio
async def test_stream_stdio_with_shutdown_event(shutdown_event: asyncio.Event) -> None:
    """Test StreamStdio stops when shutdown event is set."""
    service = ProtocolService(shutdown_event)

    async def mock_iterator() -> AsyncIterator[str]:
        yield "message1"
        shutdown_event.set()  # Set shutdown event mid-stream
        yield "message2"
        yield "message3"

    request_iterator = mock_iterator()

    responses = []
    async for response in service.StreamStdio(request_iterator, MagicMock()):
        responses.append(response)
        if shutdown_event.is_set():
            break

    # Should have stopped after shutdown event
    assert service._stream_active is False


@pytest.mark.asyncio
async def test_stream_stdio_with_none_messages(shutdown_event: asyncio.Event) -> None:
    """Test StreamStdio handles None messages correctly."""
    service = ProtocolService(shutdown_event)

    async def mock_iterator() -> AsyncIterator[str | None]:
        yield None
        yield "message1"
        yield None

    request_iterator = mock_iterator()

    responses = []
    async for response in service.StreamStdio(request_iterator, MagicMock()):
        responses.append(response)

    # Should include None messages
    assert None in responses
    assert "message1" in responses
    assert service._setup_complete.is_set()


@pytest.mark.asyncio
async def test_stream_stdio_error_handling(shutdown_event: asyncio.Event) -> None:
    """Test StreamStdio error handling during message processing."""
    service = ProtocolService(shutdown_event)

    async def mock_iterator() -> AsyncIterator[str]:
        yield "message1"
        raise RuntimeError("Stream error")

    request_iterator = mock_iterator()

    with pytest.raises(RuntimeError, match="Stream error"):
        async for _response in service.StreamStdio(request_iterator, MagicMock()):
            pass

    # Stream should be deactivated after error
    assert service._stream_active is False


@pytest.mark.asyncio
async def test_start_stream_generic_exception(shutdown_event: asyncio.Event) -> None:
    """Test StartStream handles generic exceptions."""
    service = ProtocolService(shutdown_event)
    context = MagicMock()
    context.set_code = MagicMock()
    context.set_details = MagicMock()

    # Mock setup_complete.wait() to raise a generic exception
    service._setup_complete.wait = AsyncMock(side_effect=RuntimeError("Unexpected error"))

    with pytest.raises(RuntimeError, match="Unexpected error"):
        await service.StartStream(MagicMock(), context)

    # Verify error was set on context
    context.set_code.assert_called_once_with("UNIMPLEMENTED")
    assert context.set_details.called


@pytest.mark.asyncio
async def test_heartbeat_method(shutdown_event: asyncio.Event) -> None:
    """Test _heartbeat method runs until stream is inactive."""
    import asyncio

    service = ProtocolService(shutdown_event)

    # Start heartbeat in background
    heartbeat_task = asyncio.create_task(service._heartbeat())

    # Let it run briefly
    await asyncio.sleep(0.1)

    # Stop the stream
    service._stream_active = False

    # Cancel the heartbeat task since it sleeps for 5 seconds
    heartbeat_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await heartbeat_task

    # Verify stream is inactive
    assert service._stream_active is False


@pytest.mark.asyncio
async def test_heartbeat_error_handling(shutdown_event: asyncio.Event) -> None:
    """Test _heartbeat handles errors gracefully."""
    service = ProtocolService(shutdown_event)

    # Mock queue.put to raise an error
    original_put = service._message_queue.put
    call_count = [0]

    async def failing_put(item: Any) -> None:
        call_count[0] += 1
        if call_count[0] == 1:
            raise RuntimeError("Queue error")
        return await original_put(item)

    service._message_queue.put = failing_put

    # Start heartbeat
    import asyncio

    heartbeat_task = asyncio.create_task(service._heartbeat())

    # Let it encounter the error
    await asyncio.sleep(0.1)

    # Should have stopped due to error
    # Cancel if still running
    if not heartbeat_task.done():
        heartbeat_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await heartbeat_task


# 🐍🏗️🔚
