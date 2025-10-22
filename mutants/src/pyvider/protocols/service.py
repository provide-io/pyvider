#
# pyvider/protocols/service.py
#

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

from provide.foundation import logger

from pyvider.protocols.tfprotov6.protobuf import (
    Empty,
)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class ProtocolService:
    """Service for handling plugin operations."""

    def xǁProtocolServiceǁ__init____mutmut_orig(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = asyncio.Event()
        self._stream_active = True
        self._shutdown_event = shutdown_event
        self._message_queue = asyncio.Queue()

    def xǁProtocolServiceǁ__init____mutmut_1(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = None
        self._stream_active = True
        self._shutdown_event = shutdown_event
        self._message_queue = asyncio.Queue()

    def xǁProtocolServiceǁ__init____mutmut_2(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = asyncio.Event()
        self._stream_active = None
        self._shutdown_event = shutdown_event
        self._message_queue = asyncio.Queue()

    def xǁProtocolServiceǁ__init____mutmut_3(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = asyncio.Event()
        self._stream_active = False
        self._shutdown_event = shutdown_event
        self._message_queue = asyncio.Queue()

    def xǁProtocolServiceǁ__init____mutmut_4(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = asyncio.Event()
        self._stream_active = True
        self._shutdown_event = None
        self._message_queue = asyncio.Queue()

    def xǁProtocolServiceǁ__init____mutmut_5(self, shutdown_event: asyncio.Event) -> None:
        self._setup_complete = asyncio.Event()
        self._stream_active = True
        self._shutdown_event = shutdown_event
        self._message_queue = None
    
    xǁProtocolServiceǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProtocolServiceǁ__init____mutmut_1': xǁProtocolServiceǁ__init____mutmut_1, 
        'xǁProtocolServiceǁ__init____mutmut_2': xǁProtocolServiceǁ__init____mutmut_2, 
        'xǁProtocolServiceǁ__init____mutmut_3': xǁProtocolServiceǁ__init____mutmut_3, 
        'xǁProtocolServiceǁ__init____mutmut_4': xǁProtocolServiceǁ__init____mutmut_4, 
        'xǁProtocolServiceǁ__init____mutmut_5': xǁProtocolServiceǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProtocolServiceǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁProtocolServiceǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁProtocolServiceǁ__init____mutmut_orig)
    xǁProtocolServiceǁ__init____mutmut_orig.__name__ = 'xǁProtocolServiceǁ__init__'

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_orig(self, request_iterator: Any, context: Any) -> Any:
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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_1(self, request_iterator: Any, context: Any) -> Any:
        """Handle streaming standard input/output."""
        logger.debug(None)

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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_2(self, request_iterator: Any, context: Any) -> Any:
        """Handle streaming standard input/output."""
        logger.debug("XXStreamStdio startedXX")

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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_3(self, request_iterator: Any, context: Any) -> Any:
        """Handle streaming standard input/output."""
        logger.debug("streamstdio started")

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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_4(self, request_iterator: Any, context: Any) -> Any:
        """Handle streaming standard input/output."""
        logger.debug("STREAMSTDIO STARTED")

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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_5(self, request_iterator: Any, context: Any) -> Any:
        """Handle streaming standard input/output."""
        logger.debug("StreamStdio started")

        try:

            async def process_messages() -> AsyncGenerator[Any, Any]:
                try:
                    async for message in request_iterator:
                        if self._shutdown_event.is_set():
                            return

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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_6(self, request_iterator: Any, context: Any) -> Any:
        """Handle streaming standard input/output."""
        logger.debug("StreamStdio started")

        try:

            async def process_messages() -> AsyncGenerator[Any, Any]:
                try:
                    async for message in request_iterator:
                        if self._shutdown_event.is_set():
                            break

                        logger.debug(None)

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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_7(self, request_iterator: Any, context: Any) -> Any:
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
                        if message is None:  # Changed condition
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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_8(self, request_iterator: Any, context: Any) -> Any:
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
                            await self._message_queue.put(None)

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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_9(self, request_iterator: Any, context: Any) -> Any:
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
                    logger.error(None)
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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_10(self, request_iterator: Any, context: Any) -> Any:
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
                    logger.debug(None)
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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_11(self, request_iterator: Any, context: Any) -> Any:
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
                    logger.debug("XXStreamStdio message processing completeXX")
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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_12(self, request_iterator: Any, context: Any) -> Any:
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
                    logger.debug("streamstdio message processing complete")
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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_13(self, request_iterator: Any, context: Any) -> Any:
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
                    logger.debug("STREAMSTDIO MESSAGE PROCESSING COMPLETE")
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

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_14(self, request_iterator: Any, context: Any) -> Any:
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
                    self._stream_active = None

            async for response in process_messages():
                if not self._stream_active:
                    break
                yield response

        except Exception as e:
            logger.error(f"StreamStdio outer error: {e}")
            raise
        finally:
            await self.handle_shutdown()  # Added graceful shutdown

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_15(self, request_iterator: Any, context: Any) -> Any:
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
                    self._stream_active = True

            async for response in process_messages():
                if not self._stream_active:
                    break
                yield response

        except Exception as e:
            logger.error(f"StreamStdio outer error: {e}")
            raise
        finally:
            await self.handle_shutdown()  # Added graceful shutdown

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_16(self, request_iterator: Any, context: Any) -> Any:
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
                if self._stream_active:
                    break
                yield response

        except Exception as e:
            logger.error(f"StreamStdio outer error: {e}")
            raise
        finally:
            await self.handle_shutdown()  # Added graceful shutdown

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_17(self, request_iterator: Any, context: Any) -> Any:
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
                    return
                yield response

        except Exception as e:
            logger.error(f"StreamStdio outer error: {e}")
            raise
        finally:
            await self.handle_shutdown()  # Added graceful shutdown

    # this trace made some weird stuff happen in terms of an error.

    async def xǁProtocolServiceǁStreamStdio__mutmut_18(self, request_iterator: Any, context: Any) -> Any:
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
            logger.error(None)
            raise
        finally:
            await self.handle_shutdown()  # Added graceful shutdown
    
    xǁProtocolServiceǁStreamStdio__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProtocolServiceǁStreamStdio__mutmut_1': xǁProtocolServiceǁStreamStdio__mutmut_1, 
        'xǁProtocolServiceǁStreamStdio__mutmut_2': xǁProtocolServiceǁStreamStdio__mutmut_2, 
        'xǁProtocolServiceǁStreamStdio__mutmut_3': xǁProtocolServiceǁStreamStdio__mutmut_3, 
        'xǁProtocolServiceǁStreamStdio__mutmut_4': xǁProtocolServiceǁStreamStdio__mutmut_4, 
        'xǁProtocolServiceǁStreamStdio__mutmut_5': xǁProtocolServiceǁStreamStdio__mutmut_5, 
        'xǁProtocolServiceǁStreamStdio__mutmut_6': xǁProtocolServiceǁStreamStdio__mutmut_6, 
        'xǁProtocolServiceǁStreamStdio__mutmut_7': xǁProtocolServiceǁStreamStdio__mutmut_7, 
        'xǁProtocolServiceǁStreamStdio__mutmut_8': xǁProtocolServiceǁStreamStdio__mutmut_8, 
        'xǁProtocolServiceǁStreamStdio__mutmut_9': xǁProtocolServiceǁStreamStdio__mutmut_9, 
        'xǁProtocolServiceǁStreamStdio__mutmut_10': xǁProtocolServiceǁStreamStdio__mutmut_10, 
        'xǁProtocolServiceǁStreamStdio__mutmut_11': xǁProtocolServiceǁStreamStdio__mutmut_11, 
        'xǁProtocolServiceǁStreamStdio__mutmut_12': xǁProtocolServiceǁStreamStdio__mutmut_12, 
        'xǁProtocolServiceǁStreamStdio__mutmut_13': xǁProtocolServiceǁStreamStdio__mutmut_13, 
        'xǁProtocolServiceǁStreamStdio__mutmut_14': xǁProtocolServiceǁStreamStdio__mutmut_14, 
        'xǁProtocolServiceǁStreamStdio__mutmut_15': xǁProtocolServiceǁStreamStdio__mutmut_15, 
        'xǁProtocolServiceǁStreamStdio__mutmut_16': xǁProtocolServiceǁStreamStdio__mutmut_16, 
        'xǁProtocolServiceǁStreamStdio__mutmut_17': xǁProtocolServiceǁStreamStdio__mutmut_17, 
        'xǁProtocolServiceǁStreamStdio__mutmut_18': xǁProtocolServiceǁStreamStdio__mutmut_18
    }
    
    def StreamStdio(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProtocolServiceǁStreamStdio__mutmut_orig"), object.__getattribute__(self, "xǁProtocolServiceǁStreamStdio__mutmut_mutants"), args, kwargs, self)
        return result 
    
    StreamStdio.__signature__ = _mutmut_signature(xǁProtocolServiceǁStreamStdio__mutmut_orig)
    xǁProtocolServiceǁStreamStdio__mutmut_orig.__name__ = 'xǁProtocolServiceǁStreamStdio'

    async def xǁProtocolServiceǁhandle_shutdown__mutmut_orig(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_active = False
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(0.1)  # Allow pending messages to process

    async def xǁProtocolServiceǁhandle_shutdown__mutmut_1(self, force: bool = True) -> None:
        """Handle graceful shutdown."""
        self._stream_active = False
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(0.1)  # Allow pending messages to process

    async def xǁProtocolServiceǁhandle_shutdown__mutmut_2(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_active = None
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(0.1)  # Allow pending messages to process

    async def xǁProtocolServiceǁhandle_shutdown__mutmut_3(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_active = True
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(0.1)  # Allow pending messages to process

    async def xǁProtocolServiceǁhandle_shutdown__mutmut_4(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_active = False
        if force:
            while self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(0.1)  # Allow pending messages to process

    async def xǁProtocolServiceǁhandle_shutdown__mutmut_5(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_active = False
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
        await asyncio.sleep(0.1)  # Allow pending messages to process

    async def xǁProtocolServiceǁhandle_shutdown__mutmut_6(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_active = False
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(None)  # Allow pending messages to process

    async def xǁProtocolServiceǁhandle_shutdown__mutmut_7(self, force: bool = False) -> None:
        """Handle graceful shutdown."""
        self._stream_active = False
        if force:
            while not self._message_queue.empty():
                try:
                    self._message_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        await asyncio.sleep(1.1)  # Allow pending messages to process
    
    xǁProtocolServiceǁhandle_shutdown__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProtocolServiceǁhandle_shutdown__mutmut_1': xǁProtocolServiceǁhandle_shutdown__mutmut_1, 
        'xǁProtocolServiceǁhandle_shutdown__mutmut_2': xǁProtocolServiceǁhandle_shutdown__mutmut_2, 
        'xǁProtocolServiceǁhandle_shutdown__mutmut_3': xǁProtocolServiceǁhandle_shutdown__mutmut_3, 
        'xǁProtocolServiceǁhandle_shutdown__mutmut_4': xǁProtocolServiceǁhandle_shutdown__mutmut_4, 
        'xǁProtocolServiceǁhandle_shutdown__mutmut_5': xǁProtocolServiceǁhandle_shutdown__mutmut_5, 
        'xǁProtocolServiceǁhandle_shutdown__mutmut_6': xǁProtocolServiceǁhandle_shutdown__mutmut_6, 
        'xǁProtocolServiceǁhandle_shutdown__mutmut_7': xǁProtocolServiceǁhandle_shutdown__mutmut_7
    }
    
    def handle_shutdown(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProtocolServiceǁhandle_shutdown__mutmut_orig"), object.__getattribute__(self, "xǁProtocolServiceǁhandle_shutdown__mutmut_mutants"), args, kwargs, self)
        return result 
    
    handle_shutdown.__signature__ = _mutmut_signature(xǁProtocolServiceǁhandle_shutdown__mutmut_orig)
    xǁProtocolServiceǁhandle_shutdown__mutmut_orig.__name__ = 'xǁProtocolServiceǁhandle_shutdown'

    async def xǁProtocolServiceǁStartStream__mutmut_orig(self, request: Any, context: Any) -> Empty:
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

    async def xǁProtocolServiceǁStartStream__mutmut_1(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug(None)
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

    async def xǁProtocolServiceǁStartStream__mutmut_2(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("XXStartStream calledXX")
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

    async def xǁProtocolServiceǁStartStream__mutmut_3(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("startstream called")
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

    async def xǁProtocolServiceǁStartStream__mutmut_4(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("STARTSTREAM CALLED")
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

    async def xǁProtocolServiceǁStartStream__mutmut_5(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(None, timeout=2.0)
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

    async def xǁProtocolServiceǁStartStream__mutmut_6(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=None)
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

    async def xǁProtocolServiceǁStartStream__mutmut_7(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(timeout=2.0)
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

    async def xǁProtocolServiceǁStartStream__mutmut_8(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), )
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

    async def xǁProtocolServiceǁStartStream__mutmut_9(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=3.0)
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

    async def xǁProtocolServiceǁStartStream__mutmut_10(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error(None)
            context.set_code("UNIMPLEMENTED")
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_11(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("XXTimeout waiting for StreamStdioXX")
            context.set_code("UNIMPLEMENTED")
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_12(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("timeout waiting for streamstdio")
            context.set_code("UNIMPLEMENTED")
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_13(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("TIMEOUT WAITING FOR STREAMSTDIO")
            context.set_code("UNIMPLEMENTED")
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_14(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code(None)
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_15(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code("XXUNIMPLEMENTEDXX")
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_16(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code("unimplemented")
            context.set_details("Timeout waiting for StreamStdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_17(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code("UNIMPLEMENTED")
            context.set_details(None)
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_18(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code("UNIMPLEMENTED")
            context.set_details("XXTimeout waiting for StreamStdio setupXX")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_19(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code("UNIMPLEMENTED")
            context.set_details("timeout waiting for streamstdio setup")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_20(self, request: Any, context: Any) -> Empty:
        """Handle broker stream start."""
        logger.debug("StartStream called")
        try:
            # Wait for the stream to be ready with a timeout
            await asyncio.wait_for(self._setup_complete.wait(), timeout=2.0)
            return Empty()
        except TimeoutError:
            logger.error("Timeout waiting for StreamStdio")
            context.set_code("UNIMPLEMENTED")
            context.set_details("TIMEOUT WAITING FOR STREAMSTDIO SETUP")
            raise
        except Exception as e:
            logger.error(f"StartStream error: {e}")
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_21(self, request: Any, context: Any) -> Empty:
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
            logger.error(None)
            context.set_code("UNIMPLEMENTED")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_22(self, request: Any, context: Any) -> Empty:
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
            context.set_code(None)
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_23(self, request: Any, context: Any) -> Empty:
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
            context.set_code("XXUNIMPLEMENTEDXX")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_24(self, request: Any, context: Any) -> Empty:
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
            context.set_code("unimplemented")
            context.set_details(f"Internal error: {e!s}")
            raise

    async def xǁProtocolServiceǁStartStream__mutmut_25(self, request: Any, context: Any) -> Empty:
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
            context.set_details(None)
            raise
    
    xǁProtocolServiceǁStartStream__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProtocolServiceǁStartStream__mutmut_1': xǁProtocolServiceǁStartStream__mutmut_1, 
        'xǁProtocolServiceǁStartStream__mutmut_2': xǁProtocolServiceǁStartStream__mutmut_2, 
        'xǁProtocolServiceǁStartStream__mutmut_3': xǁProtocolServiceǁStartStream__mutmut_3, 
        'xǁProtocolServiceǁStartStream__mutmut_4': xǁProtocolServiceǁStartStream__mutmut_4, 
        'xǁProtocolServiceǁStartStream__mutmut_5': xǁProtocolServiceǁStartStream__mutmut_5, 
        'xǁProtocolServiceǁStartStream__mutmut_6': xǁProtocolServiceǁStartStream__mutmut_6, 
        'xǁProtocolServiceǁStartStream__mutmut_7': xǁProtocolServiceǁStartStream__mutmut_7, 
        'xǁProtocolServiceǁStartStream__mutmut_8': xǁProtocolServiceǁStartStream__mutmut_8, 
        'xǁProtocolServiceǁStartStream__mutmut_9': xǁProtocolServiceǁStartStream__mutmut_9, 
        'xǁProtocolServiceǁStartStream__mutmut_10': xǁProtocolServiceǁStartStream__mutmut_10, 
        'xǁProtocolServiceǁStartStream__mutmut_11': xǁProtocolServiceǁStartStream__mutmut_11, 
        'xǁProtocolServiceǁStartStream__mutmut_12': xǁProtocolServiceǁStartStream__mutmut_12, 
        'xǁProtocolServiceǁStartStream__mutmut_13': xǁProtocolServiceǁStartStream__mutmut_13, 
        'xǁProtocolServiceǁStartStream__mutmut_14': xǁProtocolServiceǁStartStream__mutmut_14, 
        'xǁProtocolServiceǁStartStream__mutmut_15': xǁProtocolServiceǁStartStream__mutmut_15, 
        'xǁProtocolServiceǁStartStream__mutmut_16': xǁProtocolServiceǁStartStream__mutmut_16, 
        'xǁProtocolServiceǁStartStream__mutmut_17': xǁProtocolServiceǁStartStream__mutmut_17, 
        'xǁProtocolServiceǁStartStream__mutmut_18': xǁProtocolServiceǁStartStream__mutmut_18, 
        'xǁProtocolServiceǁStartStream__mutmut_19': xǁProtocolServiceǁStartStream__mutmut_19, 
        'xǁProtocolServiceǁStartStream__mutmut_20': xǁProtocolServiceǁStartStream__mutmut_20, 
        'xǁProtocolServiceǁStartStream__mutmut_21': xǁProtocolServiceǁStartStream__mutmut_21, 
        'xǁProtocolServiceǁStartStream__mutmut_22': xǁProtocolServiceǁStartStream__mutmut_22, 
        'xǁProtocolServiceǁStartStream__mutmut_23': xǁProtocolServiceǁStartStream__mutmut_23, 
        'xǁProtocolServiceǁStartStream__mutmut_24': xǁProtocolServiceǁStartStream__mutmut_24, 
        'xǁProtocolServiceǁStartStream__mutmut_25': xǁProtocolServiceǁStartStream__mutmut_25
    }
    
    def StartStream(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProtocolServiceǁStartStream__mutmut_orig"), object.__getattribute__(self, "xǁProtocolServiceǁStartStream__mutmut_mutants"), args, kwargs, self)
        return result 
    
    StartStream.__signature__ = _mutmut_signature(xǁProtocolServiceǁStartStream__mutmut_orig)
    xǁProtocolServiceǁStartStream__mutmut_orig.__name__ = 'xǁProtocolServiceǁStartStream'

    async def xǁProtocolServiceǁShutdown__mutmut_orig(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug("Shutdown called")
        self._stream_active = False
        self._shutdown_event.set()

        # Trigger the GracefulShutdown logic
        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()

    async def xǁProtocolServiceǁShutdown__mutmut_1(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug(None)
        self._stream_active = False
        self._shutdown_event.set()

        # Trigger the GracefulShutdown logic
        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()

    async def xǁProtocolServiceǁShutdown__mutmut_2(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug("XXShutdown calledXX")
        self._stream_active = False
        self._shutdown_event.set()

        # Trigger the GracefulShutdown logic
        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()

    async def xǁProtocolServiceǁShutdown__mutmut_3(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug("shutdown called")
        self._stream_active = False
        self._shutdown_event.set()

        # Trigger the GracefulShutdown logic
        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()

    async def xǁProtocolServiceǁShutdown__mutmut_4(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug("SHUTDOWN CALLED")
        self._stream_active = False
        self._shutdown_event.set()

        # Trigger the GracefulShutdown logic
        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()

    async def xǁProtocolServiceǁShutdown__mutmut_5(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug("Shutdown called")
        self._stream_active = None
        self._shutdown_event.set()

        # Trigger the GracefulShutdown logic
        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()

    async def xǁProtocolServiceǁShutdown__mutmut_6(self, request: Any, context: Any) -> Empty:
        """Handle shutdown request."""
        logger.debug("Shutdown called")
        self._stream_active = True
        self._shutdown_event.set()

        # Trigger the GracefulShutdown logic
        from pyvider.server import shutdown_manager

        shutdown_manager.request_shutdown()
        await shutdown_manager.shutdown_tracers()

        return Empty()
    
    xǁProtocolServiceǁShutdown__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProtocolServiceǁShutdown__mutmut_1': xǁProtocolServiceǁShutdown__mutmut_1, 
        'xǁProtocolServiceǁShutdown__mutmut_2': xǁProtocolServiceǁShutdown__mutmut_2, 
        'xǁProtocolServiceǁShutdown__mutmut_3': xǁProtocolServiceǁShutdown__mutmut_3, 
        'xǁProtocolServiceǁShutdown__mutmut_4': xǁProtocolServiceǁShutdown__mutmut_4, 
        'xǁProtocolServiceǁShutdown__mutmut_5': xǁProtocolServiceǁShutdown__mutmut_5, 
        'xǁProtocolServiceǁShutdown__mutmut_6': xǁProtocolServiceǁShutdown__mutmut_6
    }
    
    def Shutdown(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProtocolServiceǁShutdown__mutmut_orig"), object.__getattribute__(self, "xǁProtocolServiceǁShutdown__mutmut_mutants"), args, kwargs, self)
        return result 
    
    Shutdown.__signature__ = _mutmut_signature(xǁProtocolServiceǁShutdown__mutmut_orig)
    xǁProtocolServiceǁShutdown__mutmut_orig.__name__ = 'xǁProtocolServiceǁShutdown'

    async def xǁProtocolServiceǁStopStream__mutmut_orig(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug("StopStream called")
        self._stream_active = False
        return Empty()

    async def xǁProtocolServiceǁStopStream__mutmut_1(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug(None)
        self._stream_active = False
        return Empty()

    async def xǁProtocolServiceǁStopStream__mutmut_2(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug("XXStopStream calledXX")
        self._stream_active = False
        return Empty()

    async def xǁProtocolServiceǁStopStream__mutmut_3(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug("stopstream called")
        self._stream_active = False
        return Empty()

    async def xǁProtocolServiceǁStopStream__mutmut_4(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug("STOPSTREAM CALLED")
        self._stream_active = False
        return Empty()

    async def xǁProtocolServiceǁStopStream__mutmut_5(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug("StopStream called")
        self._stream_active = None
        return Empty()

    async def xǁProtocolServiceǁStopStream__mutmut_6(self, request: Any, context: Any) -> Empty:
        """Handle stream stop request."""
        logger.debug("StopStream called")
        self._stream_active = True
        return Empty()
    
    xǁProtocolServiceǁStopStream__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProtocolServiceǁStopStream__mutmut_1': xǁProtocolServiceǁStopStream__mutmut_1, 
        'xǁProtocolServiceǁStopStream__mutmut_2': xǁProtocolServiceǁStopStream__mutmut_2, 
        'xǁProtocolServiceǁStopStream__mutmut_3': xǁProtocolServiceǁStopStream__mutmut_3, 
        'xǁProtocolServiceǁStopStream__mutmut_4': xǁProtocolServiceǁStopStream__mutmut_4, 
        'xǁProtocolServiceǁStopStream__mutmut_5': xǁProtocolServiceǁStopStream__mutmut_5, 
        'xǁProtocolServiceǁStopStream__mutmut_6': xǁProtocolServiceǁStopStream__mutmut_6
    }
    
    def StopStream(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProtocolServiceǁStopStream__mutmut_orig"), object.__getattribute__(self, "xǁProtocolServiceǁStopStream__mutmut_mutants"), args, kwargs, self)
        return result 
    
    StopStream.__signature__ = _mutmut_signature(xǁProtocolServiceǁStopStream__mutmut_orig)
    xǁProtocolServiceǁStopStream__mutmut_orig.__name__ = 'xǁProtocolServiceǁStopStream'

    async def xǁProtocolServiceǁ_heartbeat__mutmut_orig(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(5)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"")  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def xǁProtocolServiceǁ_heartbeat__mutmut_1(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(None)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"")  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def xǁProtocolServiceǁ_heartbeat__mutmut_2(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(6)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"")  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def xǁProtocolServiceǁ_heartbeat__mutmut_3(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(5)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(None)  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def xǁProtocolServiceǁ_heartbeat__mutmut_4(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(5)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"XXXX")  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def xǁProtocolServiceǁ_heartbeat__mutmut_5(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(5)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"")  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def xǁProtocolServiceǁ_heartbeat__mutmut_6(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(5)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"")  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                break

    async def xǁProtocolServiceǁ_heartbeat__mutmut_7(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(5)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"")  # Empty heartbeat
            except Exception as e:
                logger.error(None)
                break

    async def xǁProtocolServiceǁ_heartbeat__mutmut_8(self) -> None:
        while self._stream_active:
            try:
                await asyncio.sleep(5)  # Send heartbeat every 5 seconds
                if self._stream_active:
                    await self._message_queue.put(b"")  # Empty heartbeat
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                return
    
    xǁProtocolServiceǁ_heartbeat__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁProtocolServiceǁ_heartbeat__mutmut_1': xǁProtocolServiceǁ_heartbeat__mutmut_1, 
        'xǁProtocolServiceǁ_heartbeat__mutmut_2': xǁProtocolServiceǁ_heartbeat__mutmut_2, 
        'xǁProtocolServiceǁ_heartbeat__mutmut_3': xǁProtocolServiceǁ_heartbeat__mutmut_3, 
        'xǁProtocolServiceǁ_heartbeat__mutmut_4': xǁProtocolServiceǁ_heartbeat__mutmut_4, 
        'xǁProtocolServiceǁ_heartbeat__mutmut_5': xǁProtocolServiceǁ_heartbeat__mutmut_5, 
        'xǁProtocolServiceǁ_heartbeat__mutmut_6': xǁProtocolServiceǁ_heartbeat__mutmut_6, 
        'xǁProtocolServiceǁ_heartbeat__mutmut_7': xǁProtocolServiceǁ_heartbeat__mutmut_7, 
        'xǁProtocolServiceǁ_heartbeat__mutmut_8': xǁProtocolServiceǁ_heartbeat__mutmut_8
    }
    
    def _heartbeat(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁProtocolServiceǁ_heartbeat__mutmut_orig"), object.__getattribute__(self, "xǁProtocolServiceǁ_heartbeat__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _heartbeat.__signature__ = _mutmut_signature(xǁProtocolServiceǁ_heartbeat__mutmut_orig)
    xǁProtocolServiceǁ_heartbeat__mutmut_orig.__name__ = 'xǁProtocolServiceǁ_heartbeat'
