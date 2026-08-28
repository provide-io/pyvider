#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The safety net under `_delegate` catches something.

It looked up its response message with `getattr(pb, f"{method}.Response")`. An
attribute name containing a dot is never an attribute, so that expression is
`None` for every method ever passed to it, and both branches that depend on it
were dead: an unhandled exception re-raised instead of becoming a diagnostic,
and an unknown method returned `None` instead of a response.
"""

from typing import Any

from provide.testkit.mocking import AsyncMock, MagicMock
import pytest

from pyvider.handler import ProviderHandler, _error_response, _response_class
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def handler() -> ProviderHandler:
    h = ProviderHandler(provider=MagicMock())
    h._ensure_provider_ready = AsyncMock(return_value=MagicMock())  # type: ignore[method-assign]
    return h


class TestResponseClassLookup:
    """The response message comes from the service descriptor, not from the method name."""

    def test_every_delegated_method_resolves_a_response(self, handler: ProviderHandler) -> None:
        rpcs = {m.name for m in pb.tfplugin6_pb2.DESCRIPTOR.services_by_name["Provider"].methods}
        unresolved = [m for m in handler._handlers if m in rpcs and _response_class(m) is None]

        assert unresolved == []

    def test_a_method_whose_message_is_named_differently_resolves(self) -> None:
        """The ValidateStateStoreConfig RPC returns a ValidateStateStore.Response.

        No lookup derived from the method name can find this one.
        """
        assert _response_class("ValidateStateStoreConfig") is pb.ValidateStateStore.Response

    def test_the_dotted_lookup_this_replaced_finds_nothing(self) -> None:
        """Pins the regression: an attribute name with a dot is never an attribute."""
        assert getattr(pb, "ReadResource.Response", None) is None
        assert _response_class("ReadResource") is pb.ReadResource.Response

    def test_a_method_that_is_not_an_rpc_resolves_to_nothing(self) -> None:
        """StreamStdio belongs to go-plugin's stdio service, not to Provider."""
        assert _response_class("StreamStdio") is None


class TestErrorResponseShape:
    """Not every response carries `diagnostics`; the two that do not still report."""

    def test_a_diagnostics_response_carries_the_error(self) -> None:
        response = _error_response("ReadResource", "Summary", "Detail")

        assert isinstance(response, pb.ReadResource.Response)
        assert len(response.diagnostics) == 1
        assert response.diagnostics[0].severity == pb.Diagnostic.ERROR
        assert response.diagnostics[0].summary == "Summary"

    def test_call_function_reports_through_its_error_field(self) -> None:
        """CallFunction.Response has `error`, a FunctionError, and no diagnostics."""
        response = _error_response("CallFunction", "Summary", "Detail")

        assert isinstance(response, pb.CallFunction.Response)
        assert "Summary" in response.error.text

    def test_stop_provider_reports_through_its_error_string(self) -> None:
        """StopProvider.Response has a single `Error` string."""
        response = _error_response("StopProvider", "Summary", "Detail")

        assert isinstance(response, pb.StopProvider.Response)
        assert "Summary" in response.Error

    def test_a_method_with_no_response_message_yields_nothing(self) -> None:
        assert _error_response("StreamStdio", "Summary", "Detail") is None


class TestDelegateSafetyNet:
    """An exception escaping a handler becomes a diagnostic, not a dropped RPC."""

    @pytest.mark.asyncio
    async def test_an_unhandled_exception_becomes_a_diagnostic(self, handler: ProviderHandler) -> None:
        async def exploding(request: Any, context: Any) -> Any:
            raise RuntimeError("handler bug")

        handler._handlers["ReadResource"] = exploding

        response = await handler._delegate("ReadResource", MagicMock(), MagicMock())

        assert isinstance(response, pb.ReadResource.Response)
        errors = [d for d in response.diagnostics if d.severity == pb.Diagnostic.ERROR]
        assert len(errors) == 1
        assert "ReadResource" in errors[0].summary

    @pytest.mark.asyncio
    async def test_an_exception_from_call_function_reaches_its_error_field(
        self, handler: ProviderHandler
    ) -> None:
        async def exploding(request: Any, context: Any) -> Any:
            raise RuntimeError("handler bug")

        handler._handlers["CallFunction"] = exploding

        response = await handler._delegate("CallFunction", MagicMock(), MagicMock())

        assert isinstance(response, pb.CallFunction.Response)
        assert "CallFunction" in response.error.text

    @pytest.mark.asyncio
    async def test_an_exception_with_no_response_message_still_propagates(
        self, handler: ProviderHandler
    ) -> None:
        """Swallowing it would leave the client waiting on a reply that never comes."""

        async def exploding(request: Any, context: Any) -> Any:
            raise RuntimeError("handler bug")

        handler._handlers["StreamStdio"] = exploding

        with pytest.raises(RuntimeError, match="handler bug"):
            await handler._delegate("StreamStdio", MagicMock(), MagicMock())

    @pytest.mark.asyncio
    async def test_an_unknown_method_is_reported_not_answered_emptily(self, handler: ProviderHandler) -> None:
        """An empty success reads as "nothing to report"; this has plenty to report."""
        handler._handlers.pop("ReadResource")

        response = await handler._delegate("ReadResource", MagicMock(), MagicMock())

        assert isinstance(response, pb.ReadResource.Response)
        errors = [d for d in response.diagnostics if d.severity == pb.Diagnostic.ERROR]
        assert len(errors) == 1
        assert "ReadResource" in errors[0].detail


# 🐍🏗️🔚
