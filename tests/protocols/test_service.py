import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock

from pyvider.protocols.service import ProtocolService


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
