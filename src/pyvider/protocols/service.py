#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from provide.foundation import logger

from pyvider.protocols.tfprotov6.protobuf import (
    Empty,
)


class ProtocolService:
    """Service for handling plugin operations."""

    def __init__(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = asyncio.Event()
        self._stream_active = True
        self._shutdown_event = shutdown_event
        self._message_queue: asyncio.Queue[Any] = asyncio.Queue()

    # this trace made some weird stuff happen in terms of an error.

    async def StreamStdio(self, request_iterator: Any, context: Any) -> Any:
        """Handle streaming standard input/output."""
        logger.debug("StreamStdio started")

        try:

            async def process_messages() -> AsyncGenerator[Any, Any]:
                try:
                    async for message in request_iterator:
                        if self._shutdown_event.is_set():
                            break

                        logger.debug(f"StreamStdio received message: {message}")

                        # Don't terminate on empty messages
                        if message is not None:  # Changed condition
                            await self._message_queue.put(message)

                        self._setup_complete.set()
                        yield message

                except Exception as e:
                    logger.error(f"StreamStdio error: {e}")
                    raise
                finally:
                    logger.debug("StreamStdio message processing complete")
                    self._stream_active = False

            async for response in process_messages():
                if not self._stream_active:
                    break
                yield response

        except Exception as e:
            logger.error(f"StreamStdio outer error: {e}")
            raise
        finally:
            await self.handle_shutdown()  # Added graceful shutdown

    async def handle_shutdown(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_active = False
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(0.1)  # Allow pending messages to process

    async def StartStream(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code("UNIMPLEMENTED")
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def Shutdown(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug("Shutdown called")
        self._stream_active = False
        self._shutdown_event.set()

        # Trigger the GracefulShutdown logic
        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()

    async def StopStream(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug("StopStream called")
        self._stream_active = False
        return Empty()

    async def _heartbeat(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(5)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"")  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break


# 🐍🏗️🔚
