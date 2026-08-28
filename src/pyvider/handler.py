#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import asyncio
from collections.abc import AsyncGenerator, AsyncIterator, Callable
import time
from typing import Any

from attrs import define, field
from provide.foundation import logger

from pyvider.observability import handler_duration, handler_errors, handler_requests
from pyvider.protocols.tfprotov6.handlers.action_handlers import stream_invoke_action
from pyvider.protocols.tfprotov6.handlers.list_resource import stream_list_resource
from pyvider.protocols.tfprotov6.handlers.state_store_handlers import (
    read_state_bytes,
    state_store_chunk_size,
    write_state_bytes,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import ProviderServicer
from pyvider.providers.base import BaseProvider


def _build_response_classes() -> dict[str, type[Any]]:
    """Map every Provider RPC to its response message, from the service descriptor.

    The method name is not enough to find it: `ValidateStateStoreConfig` returns a
    `ValidateStateStore.Response`, and no lookup derived from the name reaches
    that. The descriptor knows, and stays right when the proto changes.
    """
    service = pb.tfplugin6_pb2.DESCRIPTOR.services_by_name["Provider"]
    classes: dict[str, type[Any]] = {}
    for method in service.methods:
        # A streaming RPC answers with events rather than one response, and none
        # of them is delegated through _delegate.
        if method.server_streaming:
            continue
        # Every Provider RPC answers with a `<Message>.Response` nested inside the
        # message that names the call; a top-level output type has no containing
        # type and is not one of ours.
        container = method.output_type.containing_type
        if container is None:
            continue
        response = getattr(getattr(pb, container.name, None), "Response", None)
        if response is not None:
            classes[method.name] = response
    return classes


_RESPONSE_CLASSES: dict[str, type[Any]] = _build_response_classes()


def _response_class(method: str) -> type[Any] | None:
    """The response message for an RPC, or None for anything that is not one.

    `StreamStdio` and `StartStream` belong to go-plugin's stdio service rather
    than to Provider, so they have no response here and never had one.
    """
    return _RESPONSE_CLASSES.get(method)


def _error_response(method: str, summary: str, detail: str) -> Any | None:
    """Report an error in whichever field this RPC's response has for one.

    Most responses carry `diagnostics`. `CallFunction` carries a `FunctionError`
    instead, and `StopProvider` a bare `Error` string; a response constructed
    with a field it does not have raises, so those two are built by shape rather
    than by assumption. Returns None when the method has no response message,
    which leaves the caller to re-raise -- the only honest answer, since there is
    nothing to send.
    """
    response_class = _response_class(method)
    if response_class is None:
        return None

    fields = response_class.DESCRIPTOR.fields_by_name
    if "diagnostics" in fields:
        return response_class(
            diagnostics=[pb.Diagnostic(severity=pb.Diagnostic.ERROR, summary=summary, detail=detail)]
        )
    if "error" in fields:
        return response_class(error=pb.FunctionError(text=f"{summary}: {detail}"))
    if "Error" in fields:
        return response_class(Error=f"{summary}: {detail}")
    return response_class()


@define
class ProviderHandler(ProviderServicer):
    """Handler for provider operations that delegates to individual operation handlers.

    The _provider is lazily resolved from the hub on first use, allowing the RPC server
    to start listening immediately while provider initialization happens in the background.
    """

    _provider: BaseProvider | None = field(default=None)
    _handlers: dict[str, Callable] = field(init=False, factory=dict)
    _resolved_provider: BaseProvider | None = field(init=False, default=None)

    def __attrs_post_init__(self) -> None:
        """Initialize handler mapping."""
        from pyvider.protocols.tfprotov6.handlers import (
            ApplyResourceChangeHandler,
            CallFunctionHandler,
            CloseEphemeralResourceHandler,
            ConfigureProviderHandler,
            ConfigureStateStoreHandler,
            DeleteStateHandler,
            GenerateResourceConfigHandler,
            GetFunctionsHandler,
            GetMetadataHandler,
            GetProviderSchemaHandler,
            GetResourceIdentitySchemasHandler,
            GetStatesHandler,
            ImportResourceStateHandler,
            LockStateHandler,
            MoveResourceStateHandler,
            OpenEphemeralResourceHandler,
            PlanActionHandler,
            PlanResourceChangeHandler,
            ReadDataSourceHandler,
            ReadResourceHandler,
            RenewEphemeralResourceHandler,
            StopProviderHandler,
            UnlockStateHandler,
            UpgradeResourceIdentityHandler,
            UpgradeResourceStateHandler,
            ValidateActionConfigHandler,
            ValidateDataResourceConfigHandler,
            ValidateEphemeralResourceConfigHandler,
            ValidateListResourceConfigHandler,
            ValidateProviderConfigHandler,
            ValidateResourceConfigHandler,
            ValidateStateStoreConfigHandler,
        )

        # Map handler functions to RPC methods
        self._handlers = {
            "StreamStdio": self.StreamStdio,
            "StartStream": self.StartStream,
            "GetMetadata": GetMetadataHandler,
            "GetProviderSchema": GetProviderSchemaHandler,
            "GetResourceIdentitySchemas": GetResourceIdentitySchemasHandler,
            "ConfigureProvider": ConfigureProviderHandler,
            "ValidateProviderConfig": ValidateProviderConfigHandler,
            "StopProvider": StopProviderHandler,
            "ValidateResourceConfig": ValidateResourceConfigHandler,
            "ReadResource": ReadResourceHandler,
            "PlanResourceChange": PlanResourceChangeHandler,
            "ApplyResourceChange": ApplyResourceChangeHandler,
            "ImportResourceState": ImportResourceStateHandler,
            "UpgradeResourceState": UpgradeResourceStateHandler,
            "UpgradeResourceIdentity": UpgradeResourceIdentityHandler,
            "MoveResourceState": MoveResourceStateHandler,
            "ValidateDataResourceConfig": ValidateDataResourceConfigHandler,
            "ReadDataSource": ReadDataSourceHandler,
            "GenerateResourceConfig": GenerateResourceConfigHandler,
            "ValidateListResourceConfig": ValidateListResourceConfigHandler,
            "ValidateEphemeralResourceConfig": ValidateEphemeralResourceConfigHandler,
            "OpenEphemeralResource": OpenEphemeralResourceHandler,
            "RenewEphemeralResource": RenewEphemeralResourceHandler,
            "CloseEphemeralResource": CloseEphemeralResourceHandler,
            "ValidateActionConfig": ValidateActionConfigHandler,
            "PlanAction": PlanActionHandler,
            "GetFunctions": GetFunctionsHandler,
            "CallFunction": CallFunctionHandler,
            "ValidateStateStoreConfig": ValidateStateStoreConfigHandler,
            "ConfigureStateStore": ConfigureStateStoreHandler,
            "LockState": LockStateHandler,
            "UnlockState": UnlockStateHandler,
            "GetStates": GetStatesHandler,
            "DeleteState": DeleteStateHandler,
        }

    async def _ensure_provider_ready(self) -> BaseProvider:
        """Ensure the provider is ready, fetching from hub if necessary.

        On first call, fetches the provider from the hub. The provider is registered
        by background initialization after component discovery completes. This allows
        the RPC server to start listening immediately while initialization continues.
        """
        # Return cached provider if available
        if self._resolved_provider is not None:
            return self._resolved_provider

        # If _provider is set directly (e.g., for testing), use it
        if self._provider is not None:
            self._resolved_provider = self._provider
            return self._provider

        # Fetch provider from hub
        from pyvider.hub import DISCOVERY_READY_EVENT, hub

        # Wait for discovery to complete by waiting for the discovery ready event
        discovery_event = hub.get_component("singleton", DISCOVERY_READY_EVENT)
        if discovery_event is not None and not discovery_event.is_set():
            logger.debug(
                "Waiting for component discovery to complete",
                operation="provider_wait",
            )
            try:
                # 55 seconds: Terraform kills unresponsive plugins at 60 seconds,
                # so we fail fast with a clear error rather than letting Terraform time out silently.
                await asyncio.wait_for(discovery_event.wait(), timeout=55.0)
            except TimeoutError:
                logger.error(
                    "Component discovery timed out after 55 seconds",
                    operation="provider_wait",
                )
                raise RuntimeError(
                    "Provider initialization timed out - discovery did not complete within 55 seconds (Terraform plugin timeout is 60s)"
                ) from None

        provider = hub.get_component("singleton", "provider")
        if provider is None:
            logger.error(
                "Provider not available after discovery completed",
                operation="provider_fetch",
            )
            raise RuntimeError("Provider not available - initialization failed to complete")

        self._resolved_provider = provider
        return provider

    async def _delegate(self, method: str, request: Any, context: Any) -> Any:
        """Delegate a request to its handler."""
        # Ensure provider is ready before handling the request
        # This allows handlers to access the provider via the hub
        await self._ensure_provider_ready()

        handler = self._handlers.get(method)
        if not handler:
            logger.warning("No handler found for RPC method", method=method)
            # An empty response reads as "nothing to report", which is the opposite
            # of what an unroutable RPC means. Report it, or let gRPC report it.
            return _error_response(
                method,
                f"Unimplemented RPC {method}",
                f"This provider has no handler registered for '{method}'. "
                f"Suggestion: this is a bug in the provider, not in the configuration.",
            )

        # The individual handlers are now responsible for their own robust
        # try/except blocks. This top-level block is a final safety net.
        try:
            return await handler(request, context)
        except Exception as e:
            logger.critical(
                f"Unhandled exception escaped handler for '{method}': {e}",
                exc_info=True,
            )
            # This indicates a bug in an individual handler's error management.
            response = _error_response(
                method,
                f"Internal provider error during {method}",
                "An unhandled exception occurred. This is a bug in the provider.",
            )
            if response is not None:
                return response
            raise

    # Example: trivial “do nothing” stubs
    async def StreamStdio(self, request_iterator: Any, context: Any) -> None:
        try:
            async for _ in request_iterator:
                pass
        except Exception:
            pass  # nosec B110 - intentionally ignoring in stub handler

    async def StartStream(self, request: Any, context: Any) -> None:
        return

    async def GetMetadata(self, request: Any, context: Any) -> Any:
        return await self._delegate("GetMetadata", request, context)

    async def GetProviderSchema(self, request: Any, context: Any) -> Any:
        return await self._delegate("GetProviderSchema", request, context)

    async def GetResourceIdentitySchemas(self, request: Any, context: Any) -> Any:
        return await self._delegate("GetResourceIdentitySchemas", request, context)

    async def ConfigureProvider(self, request: Any, context: Any) -> Any:
        return await self._delegate("ConfigureProvider", request, context)

    async def ValidateProviderConfig(self, request: Any, context: Any) -> Any:
        return await self._delegate("ValidateProviderConfig", request, context)

    async def StopProvider(self, request: Any, context: Any) -> Any:
        return await self._delegate("StopProvider", request, context)

    async def ValidateResourceConfig(self, request: Any, context: Any) -> Any:
        return await self._delegate("ValidateResourceConfig", request, context)

    async def ReadResource(self, request: Any, context: Any) -> Any:
        return await self._delegate("ReadResource", request, context)

    async def PlanResourceChange(self, request: Any, context: Any) -> Any:
        return await self._delegate("PlanResourceChange", request, context)

    async def ApplyResourceChange(self, request: Any, context: Any) -> Any:
        return await self._delegate("ApplyResourceChange", request, context)

    async def ImportResourceState(self, request: Any, context: Any) -> Any:
        return await self._delegate("ImportResourceState", request, context)

    async def UpgradeResourceState(self, request: Any, context: Any) -> Any:
        return await self._delegate("UpgradeResourceState", request, context)

    async def UpgradeResourceIdentity(self, request: Any, context: Any) -> Any:
        return await self._delegate("UpgradeResourceIdentity", request, context)

    async def MoveResourceState(self, request: Any, context: Any) -> Any:
        return await self._delegate("MoveResourceState", request, context)

    async def ValidateDataResourceConfig(self, request: Any, context: Any) -> Any:
        return await self._delegate("ValidateDataResourceConfig", request, context)

    async def ReadDataSource(self, request: Any, context: Any) -> Any:
        return await self._delegate("ReadDataSource", request, context)

    async def ValidateEphemeralResourceConfig(self, request: Any, context: Any) -> Any:
        return await self._delegate("ValidateEphemeralResourceConfig", request, context)

    async def OpenEphemeralResource(self, request: Any, context: Any) -> Any:
        return await self._delegate("OpenEphemeralResource", request, context)

    async def RenewEphemeralResource(self, request: Any, context: Any) -> Any:
        return await self._delegate("RenewEphemeralResource", request, context)

    async def CloseEphemeralResource(self, request: Any, context: Any) -> Any:
        return await self._delegate("CloseEphemeralResource", request, context)

    async def GetFunctions(self, request: Any, context: Any) -> Any:
        return await self._delegate("GetFunctions", request, context)

    async def CallFunction(self, request: Any, context: Any) -> Any:
        return await self._delegate("CallFunction", request, context)

    async def GenerateResourceConfig(self, request: Any, context: Any) -> Any:
        return await self._delegate("GenerateResourceConfig", request, context)

    async def ValidateListResourceConfig(self, request: Any, context: Any) -> Any:
        return await self._delegate("ValidateListResourceConfig", request, context)

    async def ValidateActionConfig(self, request: Any, context: Any) -> Any:
        return await self._delegate("ValidateActionConfig", request, context)

    async def PlanAction(self, request: Any, context: Any) -> Any:
        return await self._delegate("PlanAction", request, context)

    async def ValidateStateStoreConfig(self, request: Any, context: Any) -> Any:
        return await self._delegate("ValidateStateStoreConfig", request, context)

    async def ConfigureStateStore(self, request: Any, context: Any) -> Any:
        return await self._delegate("ConfigureStateStore", request, context)

    async def LockState(self, request: Any, context: Any) -> Any:
        return await self._delegate("LockState", request, context)

    async def UnlockState(self, request: Any, context: Any) -> Any:
        return await self._delegate("UnlockState", request, context)

    async def GetStates(self, request: Any, context: Any) -> Any:
        return await self._delegate("GetStates", request, context)

    async def DeleteState(self, request: Any, context: Any) -> Any:
        return await self._delegate("DeleteState", request, context)

    async def ListResource(self, request: Any, context: Any) -> AsyncGenerator[pb.ListResource.Event, None]:
        start = time.perf_counter()
        handler_requests.inc(handler="ListResource")
        try:
            logger.debug(
                "ListResource RPC received",
                operation="list_resource",
                request_type=request.type_name,
                include_resource_object=request.include_resource_object,
                limit=request.limit,
            )
            async for event in stream_list_resource(request, context):
                yield event
        except Exception:
            handler_errors.inc(handler="ListResource")
            raise
        finally:
            handler_duration.observe(time.perf_counter() - start, handler="ListResource")

    async def ReadStateBytes(
        self, request: Any, context: Any
    ) -> AsyncGenerator[pb.ReadStateBytes.Response, None]:
        start = time.perf_counter()
        handler_requests.inc(handler="ReadStateBytes")
        try:
            try:
                state_bytes = await read_state_bytes(request.type_name, request.state_id) or b""
            # Not just StateStoreError: a backend can raise anything -- OSError
            # from an unreadable directory, a driver error from a remote store --
            # and an exception that escapes here reaches Terraform as a bare gRPC
            # status instead of the diagnostic built below.
            except Exception as exc:
                logger.error(
                    "ReadStateBytes failed to load state",
                    operation="read_state_bytes",
                    state_store_type=request.type_name,
                    state_id=request.state_id,
                    error_message=str(exc),
                )
                yield pb.ReadStateBytes.Response(
                    total_length=0,
                    # A range is sent on the error path for the same reason the
                    # empty-state path below sends one: Core reads
                    # `chunk.Range.End` on every chunk it receives without
                    # checking for nil, so omitting it dereferences a nil
                    # *StateRange and panics the Terraform process -- taking
                    # down the diagnostic built one line above it.
                    range=pb.StateRange(start=0, end=0),
                    diagnostics=[
                        pb.Diagnostic(
                            severity=pb.Diagnostic.ERROR,
                            summary="ReadStateBytes could not load state",
                            detail=str(exc),
                        )
                    ],
                )
                return
            chunk_size = max(1, state_store_chunk_size(request.type_name))

            logger.debug(
                "ReadStateBytes RPC received",
                operation="read_state_bytes",
                state_store_type=request.type_name,
                state_id=request.state_id,
                state_size=len(state_bytes),
            )

            if not state_bytes:
                # A range is sent even when there is nothing to send. Core reads
                # `chunk.Range.End` on every chunk it receives without checking
                # for nil, so omitting it dereferences a nil *StateRange and
                # panics the whole Terraform process -- on the very first read
                # of a workspace that does not have state yet.
                yield pb.ReadStateBytes.Response(
                    bytes=b"",
                    total_length=0,
                    range=pb.StateRange(start=0, end=0),
                    diagnostics=[],
                )
                return

            total_length = len(state_bytes)
            for start_pos in range(0, total_length, chunk_size):
                end_pos = min(start_pos + chunk_size, total_length)
                yield pb.ReadStateBytes.Response(
                    bytes=state_bytes[start_pos:end_pos],
                    total_length=total_length,
                    # `end` is the index of the last byte in the chunk, not one
                    # past it. Core writes the same form on the way in --
                    # `End: totalBytesProcessed + len(chunk) - 1` -- and decides
                    # which chunk is the last with `Range.End < TotalLength-1`,
                    # so an exclusive end shifts that boundary by one byte.
                    range=pb.StateRange(start=start_pos, end=end_pos - 1),
                    diagnostics=[],
                )
        except Exception:
            handler_errors.inc(handler="ReadStateBytes")
            raise
        finally:
            handler_duration.observe(time.perf_counter() - start, handler="ReadStateBytes")

    async def WriteStateBytes(
        self, request_iterator: AsyncIterator[Any], context: Any
    ) -> pb.WriteStateBytes.Response:
        start = time.perf_counter()
        handler_requests.inc(handler="WriteStateBytes")
        # Drain the stream to preserve protocol semantics and avoid hanging client-stream calls.
        try:
            state_chunks = bytearray()
            state_store_type = ""
            state_id = ""
            expected_total_length = 0

            async for request_chunk in request_iterator:
                # Presence, not truthiness: an unset submessage is still a
                # truthy object, and Core sends meta on the first chunk only.
                # Reading it unconditionally would blank the type name and
                # state id on every later chunk of a multi-chunk write.
                if request_chunk.HasField("meta"):
                    state_store_type = request_chunk.meta.type_name
                    state_id = request_chunk.meta.state_id
                if request_chunk.bytes:
                    state_chunks.extend(request_chunk.bytes)
                if request_chunk.total_length:
                    expected_total_length = request_chunk.total_length

            if not state_store_type or not state_id:
                return pb.WriteStateBytes.Response(
                    diagnostics=[
                        pb.Diagnostic(
                            severity=pb.Diagnostic.ERROR,
                            summary="WriteStateBytes requires request metadata",
                            detail="RequestChunk.meta must include type_name and state_id.",
                        )
                    ]
                )

            state = bytes(state_chunks)

            # Checked before the write, and that order is the whole point. A
            # stream that ends short of its declared total_length -- an aborted
            # apply, a half-closed connection, a dropped chunk -- carries a
            # truncated state, and storing it destroys the good state already
            # there. This used to write first and report the mismatch as a
            # WARNING; Terraform does not fail an apply on a warning, so the
            # apply reported success over a truncated state file.
            if expected_total_length and expected_total_length != len(state):
                logger.error(
                    "WriteStateBytes refused a truncated stream",
                    operation="write_state_bytes",
                    state_store_type=state_store_type,
                    state_id=state_id,
                    declared_length=expected_total_length,
                    received_length=len(state),
                )
                return pb.WriteStateBytes.Response(
                    diagnostics=[
                        pb.Diagnostic(
                            severity=pb.Diagnostic.ERROR,
                            summary="WriteStateBytes received a truncated stream",
                            detail=(
                                f"The stream declared {expected_total_length} bytes and delivered "
                                f"{len(state)}. Nothing was written: storing a partial state would "
                                "destroy the state already stored."
                            ),
                        )
                    ]
                )

            try:
                await write_state_bytes(state_store_type, state_id, state)
            # Not just StateStoreError, for the reason ReadStateBytes gives.
            except Exception as exc:
                logger.error(
                    "WriteStateBytes failed to persist state",
                    operation="write_state_bytes",
                    state_store_type=state_store_type,
                    state_id=state_id,
                    error_message=str(exc),
                )
                return pb.WriteStateBytes.Response(
                    diagnostics=[
                        pb.Diagnostic(
                            severity=pb.Diagnostic.ERROR,
                            summary="WriteStateBytes could not persist state",
                            detail=str(exc),
                        )
                    ]
                )

            return pb.WriteStateBytes.Response(
                diagnostics=[],
            )
        except Exception:
            handler_errors.inc(handler="WriteStateBytes")
            raise
        finally:
            handler_duration.observe(time.perf_counter() - start, handler="WriteStateBytes")

    async def InvokeAction(self, request: Any, context: Any) -> AsyncGenerator[pb.InvokeAction.Event, None]:
        start = time.perf_counter()
        handler_requests.inc(handler="InvokeAction")
        try:
            logger.debug(
                "InvokeAction RPC received",
                operation="invoke_action",
                action_type=request.action_type,
            )
            async for event in stream_invoke_action(request, context):
                yield event
        except Exception:
            handler_errors.inc(handler="InvokeAction")
            raise
        finally:
            handler_duration.observe(time.perf_counter() - start, handler="InvokeAction")


# 🐍🏗️🔚
