#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from collections.abc import Callable
from typing import Any

from attrs import define, field
from provide.foundation import logger

import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.protocols.tfprotov6.protobuf import ProviderServicer
from pyvider.providers.base import BaseProvider


@define
class ProviderHandler(ProviderServicer):
    """Handler for provider operations that delegates to individual operation handlers."""

    _provider: BaseProvider = field()
    _handlers: dict[str, Callable] = field(init=False, factory=dict)

    def __attrs_post_init__(self) -> None:
        """Initialize handler mapping."""
        from pyvider.protocols.tfprotov6.handlers import (
            ApplyResourceChangeHandler,
            CallFunctionHandler,
            CloseEphemeralResourceHandler,
            ConfigureProviderHandler,
            GetFunctionsHandler,
            GetMetadataHandler,
            GetProviderSchemaHandler,
            ImportResourceStateHandler,
            MoveResourceStateHandler,
            OpenEphemeralResourceHandler,
            PlanResourceChangeHandler,
            ReadDataSourceHandler,
            ReadResourceHandler,
            RenewEphemeralResourceHandler,
            StopProviderHandler,
            UpgradeResourceStateHandler,
            ValidateDataResourceConfigHandler,
            ValidateEphemeralResourceConfigHandler,
            ValidateProviderConfigHandler,
            ValidateResourceConfigHandler,
        )

        # Map handler functions to RPC methods
        self._handlers = {
            "StreamStdio": self.StreamStdio,
            "StartStream": self.StartStream,
            "GetMetadata": GetMetadataHandler,
            "GetProviderSchema": GetProviderSchemaHandler,
            "ConfigureProvider": ConfigureProviderHandler,
            "ValidateProviderConfig": ValidateProviderConfigHandler,
            "StopProvider": StopProviderHandler,
            "ValidateResourceConfig": ValidateResourceConfigHandler,
            "ReadResource": ReadResourceHandler,
            "PlanResourceChange": PlanResourceChangeHandler,
            "ApplyResourceChange": ApplyResourceChangeHandler,
            "ImportResourceState": ImportResourceStateHandler,
            "UpgradeResourceState": UpgradeResourceStateHandler,
            "MoveResourceState": MoveResourceStateHandler,
            "ValidateDataResourceConfig": ValidateDataResourceConfigHandler,
            "ReadDataSource": ReadDataSourceHandler,
            "ValidateEphemeralResourceConfig": ValidateEphemeralResourceConfigHandler,
            "OpenEphemeralResource": OpenEphemeralResourceHandler,
            "RenewEphemeralResource": RenewEphemeralResourceHandler,
            "CloseEphemeralResource": CloseEphemeralResourceHandler,
            "GetFunctions": GetFunctionsHandler,
            "CallFunction": CallFunctionHandler,
        }

    async def _delegate(self, method: str, request: Any, context: Any) -> Any:
        """Delegate a request to its handler."""
        handler = self._handlers.get(method)
        if not handler:
            logger.warning(f"No handler found for RPC method '{method}'.")
            # Return a default empty response if the method is unknown.
            response_class = getattr(pb, f"{method}.Response", None)
            return response_class() if response_class else None

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
            response_class = getattr(pb, f"{method}.Response", None)
            if response_class:
                return response_class(
                    diagnostics=[
                        pb.Diagnostic(
                            severity=pb.Diagnostic.ERROR,
                            summary=f"Internal provider error during {method}",
                            detail="An unhandled exception occurred. This is a bug in the provider.",
                        )
                    ]
                )
            raise

    # Example: trivial “do nothing” stubs
    async def StreamStdio(self, request_iterator: Any, context: Any) -> None:
        try:
            async for _ in request_iterator:
                pass
        except Exception:
            pass
        return

    async def StartStream(self, request: Any, context: Any) -> None:
        return

    async def GetMetadata(self, request: Any, context: Any) -> Any:
        return await self._delegate("GetMetadata", request, context)

    async def GetProviderSchema(self, request: Any, context: Any) -> Any:
        return await self._delegate("GetProviderSchema", request, context)

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


# 🐍🏗️🔚
