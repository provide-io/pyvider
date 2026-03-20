#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import asyncio
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any

from provide.foundation import logger

from pyvider.protocols.tfprotov6.protobuf import (
    Empty,
)

# Window the StartStream RPC waits for StreamStdio to signal setup-complete
# before returning UNIMPLEMENTED. Short because Terraform retries quickly.
STREAM_STARTUP_TIMEOUT_SECONDS: float = 2.0

# Cadence for the empty-message heartbeat pushed onto _message_queue while
# the stream is active.
STREAM_HEARTBEAT_INTERVAL_SECONDS: float = 5.0

# How long handle_shutdown waits after signaling shutdown so in-flight
# producers/consumers can observe the event before the task exits.
SHUTDOWN_DRAIN_SECONDS: float = 0.1


class ProtocolService:
    """Service for handling plugin operations."""

    def __init__(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = asyncio.Event()
        self._stream_stopped = asyncio.Event()
        self._shutdown_event = shutdown_event
        self._message_queue: asyncio.Queue[Any] = asyncio.Queue()

    @property
    def _stream_active(self) -> bool:
        """Compat shim for the old boolean. True while the stream is running."""
        return not self._stream_stopped.is_set()

    @_stream_active.setter
    def _stream_active(self, value: bool) -> None:
        if value:
            self._stream_stopped.clear()
        else:
            self._stream_stopped.set()

    async def StreamStdio(
        self,
        request_iterator: AsyncIterator[Any],
        context: Any,
    ) -> AsyncGenerator[Any, None]:
        """Handle streaming standard input/output.

        Reads from the inbound iterator and yields each message back to the caller.
        Terminates cleanly when the shutdown event fires or the stream is stopped.
        """
        logger.debug("StreamStdio started")
        try:

            async def process_messages() -> AsyncGenerator[Any, Any]:
                try:
                    async for message in request_iterator:
                        if self._shutdown_event.is_set():
                            break

                        logger.debug("StreamStdio received message", message=str(message))

                        # Don't terminate on empty messages
                        if message is not None:  # Changed condition
                            await self._message_queue.put(message)

                        self._setup_complete.set()
                        yield message

                except Exception as e:
                    logger.error("StreamStdio error", error=str(e))
                    raise
                finally:
                    logger.debug("StreamStdio message processing complete")
                    self._stream_active = False

            async for response in process_messages():
                if not self._stream_active:
                    break

                logger.debug("StreamStdio received message", message=str(message))

                if message is not None:
                    await self._message_queue.put(message)

                self._setup_complete.set()
                yield message
        except Exception as e:
            logger.error("StreamStdio outer error", error=str(e))
            raise
        finally:
            logger.debug("StreamStdio message processing complete")
            self._stream_stopped.set()
            await self.handle_shutdown()

    async def handle_shutdown(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_stopped.set()
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(SHUTDOWN_DRAIN_SECONDS)

    async def StartStream(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            await asyncio.wait_for(self._setup_complete.wait(), timeout=STREAM_STARTUP_TIMEOUT_SECONDS)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code("UNIMPLEMENTED")
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error("StartStream error", error=str(e))
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def Shutdown(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug("Shutdown called")
        self._stream_stopped.set()
        self._shutdown_event.set()

        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()

    async def StopStream(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug("StopStream called")
        self._stream_stopped.set()
        return Empty()

    async def _heartbeat(self) -> None:
        while not self._stream_stopped.is_set():
            try:
                await asyncio.sleep(STREAM_HEARTBEAT_INTERVAL_SECONDS)
                if not self._stream_stopped.is_set():
                    await self._message_queue.put(b"")
            except Exception as e:
                logger.error("Heartbeat error", error=str(e))
                break


# 🐍🏗️🔚
