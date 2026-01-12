#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ProviderHandler - Resource and data source operations."""

from provide.testkit.mocking import AsyncMock, MagicMock
import pytest

from pyvider.handler import ProviderHandler


@pytest.fixture
def mock_provider() -> MagicMock:
    return MagicMock()


@pytest.mark.asyncio
async def test_validate_resource_config_delegates(mock_provider: MagicMock) -> None:
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
async def test_read_resource_delegates(mock_provider: MagicMock) -> None:
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
async def test_plan_resource_change_delegates(mock_provider: MagicMock) -> None:
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
async def test_apply_resource_change_delegates(mock_provider: MagicMock) -> None:
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
async def test_import_resource_state_delegates(mock_provider: MagicMock) -> None:
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
async def test_upgrade_resource_state_delegates(mock_provider: MagicMock) -> None:
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
async def test_move_resource_state_delegates(mock_provider: MagicMock) -> None:
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
async def test_validate_data_resource_config_delegates(mock_provider: MagicMock) -> None:
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
async def test_read_data_source_delegates(mock_provider: MagicMock) -> None:
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
async def test_validate_ephemeral_resource_config_delegates(mock_provider: MagicMock) -> None:
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
async def test_open_ephemeral_resource_delegates(mock_provider: MagicMock) -> None:
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
async def test_renew_ephemeral_resource_delegates(mock_provider: MagicMock) -> None:
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
async def test_close_ephemeral_resource_delegates(mock_provider: MagicMock) -> None:
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
async def test_get_functions_delegates(mock_provider: MagicMock) -> None:
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
async def test_call_function_delegates(mock_provider: MagicMock) -> None:
    """Test CallFunction delegates to handler."""
    handler = ProviderHandler(provider=mock_provider)

    mock_delegate = AsyncMock(return_value="call_response")
    handler._delegate = mock_delegate

    request = MagicMock()
    context = MagicMock()

    result = await handler.CallFunction(request, context)

    mock_delegate.assert_awaited_once_with("CallFunction", request, context)
    assert result == "call_response"


# 🐍🏗️🔚
