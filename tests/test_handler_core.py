#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from collections.abc import AsyncGenerator

from provide.testkit.mocking import AsyncMock, MagicMock, patch
import pytest

from pyvider.handler import ProviderHandler
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def mock_provider() -> MagicMock:
    return MagicMock()


def test_post_init(mock_provider: MagicMock) -> None:
    handler = ProviderHandler(provider=mock_provider)

    assert "GetMetadata" in handler._handlers

    assert "GetProviderSchema" in handler._handlers

    assert "GetResourceIdentitySchemas" in handler._handlers

    assert "ConfigureProvider" in handler._handlers

    assert "ValidateProviderConfig" in handler._handlers

    assert "StopProvider" in handler._handlers

    assert "ValidateResourceConfig" in handler._handlers

    assert "ReadResource" in handler._handlers

    assert "PlanResourceChange" in handler._handlers

    assert "ApplyResourceChange" in handler._handlers

    assert "ImportResourceState" in handler._handlers

    assert "UpgradeResourceState" in handler._handlers

    assert "UpgradeResourceIdentity" in handler._handlers

    assert "MoveResourceState" in handler._handlers

    assert "ValidateDataResourceConfig" in handler._handlers

    assert "ReadDataSource" in handler._handlers

    assert "ValidateEphemeralResourceConfig" in handler._handlers

    assert "OpenEphemeralResource" in handler._handlers

    assert "RenewEphemeralResource" in handler._handlers

    assert "CloseEphemeralResource" in handler._handlers

    assert "GetFunctions" in handler._handlers

    assert "CallFunction" in handler._handlers

    assert "GenerateResourceConfig" in handler._handlers

    assert "ValidateListResourceConfig" in handler._handlers

    assert "ValidateStateStoreConfig" in handler._handlers

    assert "ConfigureStateStore" in handler._handlers

    assert "LockState" in handler._handlers

    assert "UnlockState" in handler._handlers

    assert "GetStates" in handler._handlers

    assert "DeleteState" in handler._handlers

    assert "PlanAction" in handler._handlers

    assert "ValidateActionConfig" in handler._handlers


@pytest.mark.asyncio
async def test_delegate_success(mock_provider: MagicMock) -> None:
    handler = ProviderHandler(provider=mock_provider)

    mock_handler = AsyncMock(return_value="success")

    handler._handlers = {"TestMethod": mock_handler}

    request = MagicMock()

    context = MagicMock()

    response = await handler._delegate("TestMethod", request, context)

    mock_handler.assert_awaited_once_with(request, context)

    assert response == "success"


@pytest.mark.asyncio
async def test_delegate_no_handler(mock_provider: MagicMock) -> None:
    """An RPC with no handler is reported through the response it does have.

    This used to patch `pyvider.handler.getattr` and assert it was called with
    "UnknownMethod.Response" -- asserting the expression rather than the result,
    with a mock standing in for the None that expression always returned. The
    dead branch looked alive for as long as the mock was there.
    """
    handler = ProviderHandler(provider=mock_provider)

    handler._handlers = {}  # empty handlers

    response = await handler._delegate("ReadResource", MagicMock(), MagicMock())

    assert isinstance(response, pb.ReadResource.Response)
    assert [d for d in response.diagnostics if d.severity == pb.Diagnostic.ERROR]


@pytest.mark.asyncio
async def test_delegate_unhandled_exception(mock_provider: MagicMock) -> None:
    """An exception escaping a handler becomes a diagnostic on that RPC's response.

    Same rewrite as test_delegate_no_handler above: the patched `getattr` was
    supplying a response class the real code could never obtain, so this asserted
    that a branch was reachable when it was not.
    """
    handler = ProviderHandler(provider=mock_provider)

    handler._handlers = {"ReadResource": AsyncMock(side_effect=Exception("test error"))}

    response = await handler._delegate("ReadResource", MagicMock(), MagicMock())

    assert isinstance(response, pb.ReadResource.Response)
    errors = [d for d in response.diagnostics if d.severity == pb.Diagnostic.ERROR]
    assert len(errors) == 1
    assert "ReadResource" in errors[0].summary


@pytest.mark.asyncio
async def test_delegate_exception_no_response_class(mock_provider: MagicMock) -> None:
    """Test that exception is re-raised when response class cannot be found."""

    handler = ProviderHandler(provider=mock_provider)

    mock_handler = AsyncMock(side_effect=Exception("test error"))

    handler._handlers = {"TestMethod": mock_handler}

    request = MagicMock()

    context = MagicMock()

    # Mock getattr to return None (no response class found)

    with patch("pyvider.handler.getattr", return_value=None), pytest.raises(Exception, match="test error"):
        await handler._delegate("TestMethod", request, context)


@pytest.mark.asyncio
async def test_stream_stdio(mock_provider: MagicMock) -> None:
    """Test StreamStdio handler consumes request_iterator."""

    handler = ProviderHandler(provider=mock_provider)

    # Create an async iterator

    async def async_iterator() -> AsyncGenerator[int, None]:
        for i in range(3):
            yield i

    context = MagicMock()

    result = await handler.StreamStdio(async_iterator(), context)

    # Should return None

    assert result is None


@pytest.mark.asyncio
async def test_stream_stdio_exception_handling(mock_provider: MagicMock) -> None:
    """Test StreamStdio handles exceptions gracefully."""

    handler = ProviderHandler(provider=mock_provider)

    # Create an async iterator that raises

    async def async_iterator_with_error() -> AsyncGenerator[int, None]:
        yield 1

        raise RuntimeError("iterator error")

    context = MagicMock()

    result = await handler.StreamStdio(async_iterator_with_error(), context)

    # Should still return None despite exception

    assert result is None


@pytest.mark.asyncio
async def test_start_stream(mock_provider: MagicMock) -> None:
    """Test StartStream handler."""

    handler = ProviderHandler(provider=mock_provider)

    request = MagicMock()

    context = MagicMock()

    result = await handler.StartStream(request, context)

    # Should return None

    assert result is None


# Test all RPC method wrappers delegate correctly


@pytest.mark.asyncio
async def test_get_metadata_delegates(mock_provider: MagicMock) -> None:
    """Test GetMetadata delegates to handler."""

    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="metadata_response")

    handler._delegate = mock_delegate

    request = MagicMock()

    context = MagicMock()

    result = await handler.GetMetadata(request, context)

    mock_delegate.assert_awaited_once_with("GetMetadata", request, context)

    assert result == "metadata_response"


@pytest.mark.asyncio
async def test_get_provider_schema_delegates(mock_provider: MagicMock) -> None:
    """Test GetProviderSchema delegates to handler."""

    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="schema_response")

    handler._delegate = mock_delegate

    request = MagicMock()

    context = MagicMock()

    result = await handler.GetProviderSchema(request, context)

    mock_delegate.assert_awaited_once_with("GetProviderSchema", request, context)

    assert result == "schema_response"


@pytest.mark.asyncio
async def test_get_resource_identity_schemas_delegates(mock_provider: MagicMock) -> None:
    """Test GetResourceIdentitySchemas delegates to handler."""

    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="identity_schemas_response")

    handler._delegate = mock_delegate

    request = MagicMock()

    context = MagicMock()

    result = await handler.GetResourceIdentitySchemas(request, context)

    mock_delegate.assert_awaited_once_with("GetResourceIdentitySchemas", request, context)

    assert result == "identity_schemas_response"


@pytest.mark.asyncio
async def test_upgrade_resource_identity_delegates(mock_provider: MagicMock) -> None:
    """Test UpgradeResourceIdentity delegates to handler."""

    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="upgrade_identity_response")

    handler._delegate = mock_delegate

    request = MagicMock()

    context = MagicMock()

    result = await handler.UpgradeResourceIdentity(request, context)

    mock_delegate.assert_awaited_once_with("UpgradeResourceIdentity", request, context)

    assert result == "upgrade_identity_response"


@pytest.mark.asyncio
async def test_configure_provider_delegates(mock_provider: MagicMock) -> None:
    """Test ConfigureProvider delegates to handler."""

    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="config_response")

    handler._delegate = mock_delegate

    request = MagicMock()

    context = MagicMock()

    result = await handler.ConfigureProvider(request, context)

    mock_delegate.assert_awaited_once_with("ConfigureProvider", request, context)

    assert result == "config_response"


@pytest.mark.asyncio
async def test_validate_provider_config_delegates(mock_provider: MagicMock) -> None:
    """Test ValidateProviderConfig delegates to handler."""

    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="validate_response")

    handler._delegate = mock_delegate

    request = MagicMock()

    context = MagicMock()

    result = await handler.ValidateProviderConfig(request, context)

    mock_delegate.assert_awaited_once_with("ValidateProviderConfig", request, context)

    assert result == "validate_response"


@pytest.mark.asyncio
async def test_stop_provider_delegates(mock_provider: MagicMock) -> None:
    """Test StopProvider delegates to handler."""

    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="stop_response")

    handler._delegate = mock_delegate

    request = MagicMock()

    context = MagicMock()

    result = await handler.StopProvider(request, context)

    mock_delegate.assert_awaited_once_with("StopProvider", request, context)

    assert result == "stop_response"


# 🐍🏗️🔚
