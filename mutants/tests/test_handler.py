from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pyvider.handler import ProviderHandler
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def mock_provider():
    return MagicMock()


def test_post_init(mock_provider):
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
async def test_delegate_success(mock_provider):
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
    handler = ProviderHandler(provider=mock_provider)
    handler._handlers = {}  # empty handlers

    request = MagicMock()
    context = MagicMock()

    # Mock getattr to return a mock response class
    with patch("pyvider.handler.getattr", return_value=MagicMock()) as mock_getattr:
        response = await handler._delegate("UnknownMethod", request, context)
        mock_getattr.assert_called_once_with(pb, "UnknownMethod.Response", None)
        assert response is not None


@pytest.mark.asyncio
async def test_delegate_unhandled_exception(mock_provider):
    handler = ProviderHandler(provider=mock_provider)

    mock_handler = AsyncMock(side_effect=Exception("test error"))
    handler._handlers = {"TestMethod": mock_handler}

    request = MagicMock()
    context = MagicMock()

    response_class_mock = MagicMock()
    response_instance_mock = MagicMock()
    response_class_mock.return_value = response_instance_mock

    with patch("pyvider.handler.getattr", return_value=response_class_mock) as mock_getattr:
        response = await handler._delegate("TestMethod", request, context)

        mock_getattr.assert_called_with(pb, "TestMethod.Response", None)

        response_class_mock.assert_called_once()
        _, kwargs = response_class_mock.call_args
        assert "diagnostics" in kwargs
        assert len(kwargs["diagnostics"]) == 1
        assert kwargs["diagnostics"][0].severity == 1  # ERROR
        assert "Internal provider error" in kwargs["diagnostics"][0].summary

        assert response == response_instance_mock


@pytest.mark.asyncio
async def test_delegate_exception_no_response_class(mock_provider):
    """Test that exception is re-raised when response class cannot be found."""
    handler = ProviderHandler(provider=mock_provider)

    mock_handler = AsyncMock(side_effect=Exception("test error"))
    handler._handlers = {"TestMethod": mock_handler}

    request = MagicMock()
    context = MagicMock()

    # Mock getattr to return None (no response class found)
    with patch("pyvider.handler.getattr", return_value=None):
        with pytest.raises(Exception, match="test error"):
            await handler._delegate("TestMethod", request, context)


@pytest.mark.asyncio
async def test_stream_stdio(mock_provider):
    """Test StreamStdio handler consumes request_iterator."""
    handler = ProviderHandler(provider=mock_provider)

    # Create an async iterator
    async def async_iterator():
        for i in range(3):
            yield i

    context = MagicMock()
    result = await handler.StreamStdio(async_iterator(), context)

    # Should return None
    assert result is None


@pytest.mark.asyncio
async def test_stream_stdio_exception_handling(mock_provider):
    """Test StreamStdio handles exceptions gracefully."""
    handler = ProviderHandler(provider=mock_provider)

    # Create an async iterator that raises
    async def async_iterator_with_error():
        yield 1
        raise RuntimeError("iterator error")

    context = MagicMock()
    result = await handler.StreamStdio(async_iterator_with_error(), context)

    # Should still return None despite exception
    assert result is None


@pytest.mark.asyncio
async def test_start_stream(mock_provider):
    """Test StartStream handler."""
    handler = ProviderHandler(provider=mock_provider)

    request = MagicMock()
    context = MagicMock()

    result = await handler.StartStream(request, context)

    # Should return None
    assert result is None


# Test all RPC method wrappers delegate correctly
@pytest.mark.asyncio
async def test_get_metadata_delegates(mock_provider):
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
async def test_get_provider_schema_delegates(mock_provider):
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
async def test_configure_provider_delegates(mock_provider):
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
async def test_validate_provider_config_delegates(mock_provider):
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
async def test_stop_provider_delegates(mock_provider):
    """Test StopProvider delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="stop_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.StopProvider(request, context)

    mock_delegate.assert_awaited_once_with("StopProvider", request, context)
    assert result == "stop_response"


@pytest.mark.asyncio
async def test_validate_resource_config_delegates(mock_provider):
    """Test ValidateResourceConfig delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="validate_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.ValidateResourceConfig(request, context)

    mock_delegate.assert_awaited_once_with("ValidateResourceConfig", request, context)
    assert result == "validate_response"


@pytest.mark.asyncio
async def test_read_resource_delegates(mock_provider):
    """Test ReadResource delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="read_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.ReadResource(request, context)

    mock_delegate.assert_awaited_once_with("ReadResource", request, context)
    assert result == "read_response"


@pytest.mark.asyncio
async def test_plan_resource_change_delegates(mock_provider):
    """Test PlanResourceChange delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="plan_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.PlanResourceChange(request, context)

    mock_delegate.assert_awaited_once_with("PlanResourceChange", request, context)
    assert result == "plan_response"


@pytest.mark.asyncio
async def test_apply_resource_change_delegates(mock_provider):
    """Test ApplyResourceChange delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="apply_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.ApplyResourceChange(request, context)

    mock_delegate.assert_awaited_once_with("ApplyResourceChange", request, context)
    assert result == "apply_response"


@pytest.mark.asyncio
async def test_import_resource_state_delegates(mock_provider):
    """Test ImportResourceState delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="import_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.ImportResourceState(request, context)

    mock_delegate.assert_awaited_once_with("ImportResourceState", request, context)
    assert result == "import_response"


@pytest.mark.asyncio
async def test_upgrade_resource_state_delegates(mock_provider):
    """Test UpgradeResourceState delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="upgrade_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.UpgradeResourceState(request, context)

    mock_delegate.assert_awaited_once_with("UpgradeResourceState", request, context)
    assert result == "upgrade_response"


@pytest.mark.asyncio
async def test_move_resource_state_delegates(mock_provider):
    """Test MoveResourceState delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="move_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.MoveResourceState(request, context)

    mock_delegate.assert_awaited_once_with("MoveResourceState", request, context)
    assert result == "move_response"


@pytest.mark.asyncio
async def test_validate_data_resource_config_delegates(mock_provider):
    """Test ValidateDataResourceConfig delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="validate_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.ValidateDataResourceConfig(request, context)

    mock_delegate.assert_awaited_once_with("ValidateDataResourceConfig", request, context)
    assert result == "validate_response"


@pytest.mark.asyncio
async def test_read_data_source_delegates(mock_provider):
    """Test ReadDataSource delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="read_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.ReadDataSource(request, context)

    mock_delegate.assert_awaited_once_with("ReadDataSource", request, context)
    assert result == "read_response"


@pytest.mark.asyncio
async def test_validate_ephemeral_resource_config_delegates(mock_provider):
    """Test ValidateEphemeralResourceConfig delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="validate_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.ValidateEphemeralResourceConfig(request, context)

    mock_delegate.assert_awaited_once_with("ValidateEphemeralResourceConfig", request, context)
    assert result == "validate_response"


@pytest.mark.asyncio
async def test_open_ephemeral_resource_delegates(mock_provider):
    """Test OpenEphemeralResource delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="open_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.OpenEphemeralResource(request, context)

    mock_delegate.assert_awaited_once_with("OpenEphemeralResource", request, context)
    assert result == "open_response"


@pytest.mark.asyncio
async def test_renew_ephemeral_resource_delegates(mock_provider):
    """Test RenewEphemeralResource delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="renew_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.RenewEphemeralResource(request, context)

    mock_delegate.assert_awaited_once_with("RenewEphemeralResource", request, context)
    assert result == "renew_response"


@pytest.mark.asyncio
async def test_close_ephemeral_resource_delegates(mock_provider):
    """Test CloseEphemeralResource delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="close_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.CloseEphemeralResource(request, context)

    mock_delegate.assert_awaited_once_with("CloseEphemeralResource", request, context)
    assert result == "close_response"


@pytest.mark.asyncio
async def test_get_functions_delegates(mock_provider):
    """Test GetFunctions delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="functions_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.GetFunctions(request, context)

    mock_delegate.assert_awaited_once_with("GetFunctions", request, context)
    assert result == "functions_response"


@pytest.mark.asyncio
async def test_call_function_delegates(mock_provider):
    """Test CallFunction delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="call_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.CallFunction(request, context)

    mock_delegate.assert_awaited_once_with("CallFunction", request, context)
    assert result == "call_response"
