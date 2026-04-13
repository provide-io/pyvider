#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TDD Test for the GetProviderSchemaHandler Caching Mechanism.

This test defines the contract for the schema caching logic, ensuring that
the expensive schema computation is performed exactly once, even under
concurrent load. This validates the pattern of using asyncio.Future to
handle a "compute-once, await-many" scenario, which is more robust and
idiomatic than using a simple lock for this purpose."""

import asyncio
from collections.abc import AsyncIterator
from typing import Any

from provide.testkit.mocking import AsyncMock
import pytest
from pytest_mock import MockerFixture

from pyvider.hub import hub
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.providers.base import BaseProvider, ProviderMetadata
from pyvider.schema import s_provider


@pytest.fixture
async def mock_provider_in_hub(mocker: MockerFixture) -> AsyncIterator[None]:
    """
    A fixture to ensure a minimal, valid provider is registered in the hub
    so that the handler can find it.
    """
    # Create a mock provider instance with a minimal valid schema
    provider = BaseProvider(metadata=ProviderMetadata(name="test", version="0.0.1"))
    provider._final_schema = s_provider()

    # Register it in the hub
    hub.register("singleton", "provider", provider)
    yield
    # Clean up the hub after the test
    hub._registry.clear(dimension="singleton")


@pytest.mark.asyncio
async def test_get_provider_schema_handler_avoids_race_condition(
    mocker: MockerFixture, mock_provider_in_hub: Any
) -> None:
    """
    TDD Contract: Verifies that even with many concurrent requests, the
    underlying schema computation is only ever executed once.
    """
    # --- Arrange ---

    # 1. Import the real handler we are testing.
    from pyvider.protocols.tfprotov6.handlers.get_provider_schema import (
        GetProviderSchemaHandler,
    )

    # 2. Create a mock for the expensive computation function. We will use this
    #    to count how many times it gets called.
    mock_compute_schema = AsyncMock(return_value=pb.GetProviderSchema.Response())
    mocker.patch(
        "pyvider.protocols.tfprotov6.handlers.get_provider_schema._compute_schema_once",
        new=mock_compute_schema,
    )

    # 3. Create a number of concurrent tasks that will all call the handler
    #    at the same time, simulating a "stampeding herd".
    num_concurrent_requests = 20
    dummy_request = pb.GetProviderSchema.Request()

    tasks = [
        asyncio.create_task(GetProviderSchemaHandler(dummy_request, context=None))
        for _ in range(num_concurrent_requests)
    ]

    # --- Act ---

    # 4. Run all the concurrent handler calls.
    results = await asyncio.gather(*tasks)

    # --- Assert ---

    # 5. The core assertion: The expensive computation function must have been
    #    called exactly one time.
    mock_compute_schema.assert_called_once()

    # 6. Sanity check: Ensure all concurrent callers received a valid and
    #    identical response object.
    assert len(results) == num_concurrent_requests
    first_result = results[0]
    assert isinstance(first_result, pb.GetProviderSchema.Response)
    for result in results:
        assert result is first_result


# 🐍🏗️🔚
