#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The process-lifetime schema cache must survive one bad call.

GetProviderSchema is answered from a Future shared by every caller, for the life
of the plugin process. A single cancelled or failed call must not leave that
Future in a state the next caller inherits -- a provider that cannot serve its
schema cannot be used at all.
"""

from __future__ import annotations

import asyncio
from collections.abc import Iterator

import pytest

from pyvider.protocols.tfprotov6.handlers import get_provider_schema as gps
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture(autouse=True)
def _clear_cache() -> Iterator[None]:
    gps._schema_future = None
    gps._task = None
    yield
    gps._schema_future = None
    gps._task = None


async def _call() -> pb.GetProviderSchema.Response:
    return await gps._get_provider_schema_impl(pb.GetProviderSchema.Request(), None)


@pytest.fixture
def good_schema(monkeypatch: pytest.MonkeyPatch) -> pb.GetProviderSchema.Response:
    """A successful computation, so the caching path is exercised rather than the error path.

    Nothing is registered in a bare test process, so the real computation
    produces an ERROR diagnostic -- which is deliberately not cached.
    """
    response = pb.GetProviderSchema.Response(provider=pb.Schema(version=1))

    async def _compute() -> pb.GetProviderSchema.Response:
        await asyncio.sleep(0)
        return response

    monkeypatch.setattr(gps, "_compute_schema_once", _compute)
    return response


async def test_a_cancelled_caller_does_not_poison_the_cache(
    good_schema: pb.GetProviderSchema.Response,
) -> None:
    """Terraform cancelling one call must not disable the schema for every later one."""
    first = asyncio.create_task(_call())
    await asyncio.sleep(0)  # let it reach the await on the shared Future
    first.cancel()
    with pytest.raises(asyncio.CancelledError):
        await first

    # The next caller must still get a schema.
    response = await asyncio.wait_for(_call(), timeout=10)
    assert response == good_schema


async def test_a_cancelled_caller_leaves_other_waiters_alone(
    good_schema: pb.GetProviderSchema.Response,
) -> None:
    """Two callers share one Future; cancelling one must not cancel the other."""
    first = asyncio.create_task(_call())
    second = asyncio.create_task(_call())
    await asyncio.sleep(0)

    first.cancel()
    with pytest.raises(asyncio.CancelledError):
        await first

    assert await asyncio.wait_for(second, timeout=10) == good_schema


async def test_a_successful_schema_is_still_cached(
    good_schema: pb.GetProviderSchema.Response,
) -> None:
    """The cache has to keep being a cache."""
    first = await _call()
    cached = gps._schema_future
    second = await _call()

    assert cached is gps._schema_future, "the Future was rebuilt for a second caller"
    assert first is second is good_schema


async def test_a_failed_computation_is_not_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    """A hub not yet populated when the first call lands must not fail every later call."""
    calls = 0

    async def _flaky() -> pb.GetProviderSchema.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("hub not ready")
        return pb.GetProviderSchema.Response(provider=pb.Schema(version=1))

    monkeypatch.setattr(gps, "_compute_schema_once", _flaky)

    with pytest.raises(RuntimeError):
        await _call()

    assert gps._schema_future is None, "a failure was cached for the life of the process"
    assert (await _call()).provider.version == 1


# 🌊🪢🔚
