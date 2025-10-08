import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from pyvider.handler import ProviderHandler


@pytest.fixture
def mock_provider():
    return MagicMock()


    handler = ProviderHandler(provider=mock_provider)
    assert "GetMetadata" in handler._handlers
    assert "GetProviderSchema" in handler._handlers
    assert "ConfigureProvider" in handler._handlers
    assert "ValidateProviderConfig" in handler._handlers
    assert "StopProvider" in handler._handlers
    assert "ValidateResourceConfig" in handler._handlers
    assert "ReadResource" in handler._handlers
    assert "PlanResourceChange" in handler._handlers
    assert "ApplyResourceChange" in handler._handlers
    assert "ImportResourceState" in handler._handlers
    assert "UpgradeResourceState" in handler._handlers
    assert "MoveResourceState" in handler._handlers
    assert "ValidateDataResourceConfig" in handler._handlers
    assert "ReadDataSource" in handler._handlers
    assert "ValidateEphemeralResourceConfig" in handler._handlers
    assert "OpenEphemeralResource" in handler._handlers
    assert "RenewEphemeralResource" in handler._handlers
    assert "CloseEphemeralResource" in handler._handlers
    assert "GetFunctions" in handler._handlers
    assert "CallFunction" in handler._handlers


@pytest.mark.asyncio
    handler = ProviderHandler(provider=mock_provider)

    mock_handler = AsyncMock(return_value="success")
    handler._handlers = {"TestMethod": mock_handler}

    request = MagicMock()
    context = MagicMock()

    response = await handler._delegate("TestMethod", request, context)

    mock_handler.assert_awaited_once_with(request, context)
    assert response == "success"


@pytest.mark.asyncio
async def test_delegate_no_handler(mock_provider):
    handler = ProviderHandler(_provider=mock_provider)
    handler._handlers = {}  # empty handlers

    request = MagicMock()
    context = MagicMock()

    # Mock getattr to return a mock response class
    with patch("pyvider.handler.getattr", return_value=MagicMock()) as mock_getattr:
        response = await handler._delegate("UnknownMethod", request, context)
        mock_getattr.assert_called_once_with(
            __import__("pyvider.protocols.tfprotov6.protobuf"), "UnknownMethod.Response", None
        )
        assert response is not None


@pytest.mark.asyncio
async def test_delegate_unhandled_exception(mock_provider):
    handler = ProviderHandler(_provider=mock_provider)

    mock_handler = AsyncMock(side_effect=Exception("test error"))
    handler._handlers = {"TestMethod": mock_handler}

    request = MagicMock()
    context = MagicMock()

    with patch("pyvider.handler.getattr", return_value=MagicMock()) as mock_getattr:
        response = await handler._delegate("TestMethod", request, context)
        mock_getattr.assert_called_with(
            __import__("pyvider.protocols.tfprotov6.protobuf"), "TestMethod.Response", None
        )
        assert response is not None
        # check diagnostics
        assert len(response.diagnostics) == 1
        assert response.diagnostics[0].severity == 1  # ERROR
        assert "Internal provider error" in response.diagnostics[0].summary
