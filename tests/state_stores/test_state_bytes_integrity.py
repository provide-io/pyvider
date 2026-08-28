#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""State bytes that reach Core, and state bytes that must never reach disk.

Both rules here are read out of Terraform rather than out of the proto: Core
dereferences `chunk.Range.End` without a nil check, and it does not fail an
apply on a WARNING.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest

from pyvider.handler import ProviderHandler
from pyvider.protocols.tfprotov6.handlers.state_store_handlers import reset_state_stores
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.state_stores import FileSystemStateStore, state_store_manager

TYPE_NAME = "integrity_store"
STATE_ID = "default"


@pytest.fixture(autouse=True)
def _reset_manager() -> Iterator[None]:
    reset_state_stores()
    yield
    reset_state_stores()


@pytest.fixture
def backend(tmp_path: Path) -> FileSystemStateStore:
    store = FileSystemStateStore(root=tmp_path / "state")
    state_store_manager.register_instance(TYPE_NAME, store)
    return store


async def _write(
    handler: ProviderHandler, payload: bytes, *, declared: int | None = None
) -> pb.WriteStateBytes.Response:
    async def chunks() -> AsyncIterator[pb.WriteStateBytes.RequestChunk]:
        yield pb.WriteStateBytes.RequestChunk(
            meta=pb.RequestChunkMeta(type_name=TYPE_NAME, state_id=STATE_ID),
            bytes=payload,
            total_length=len(payload) if declared is None else declared,
            range=pb.StateRange(start=0, end=max(len(payload) - 1, 0)),
        )

    return await handler.WriteStateBytes(chunks(), context=None)


def _severities(response: pb.WriteStateBytes.Response) -> list[int]:
    return [diagnostic.severity for diagnostic in response.diagnostics]


class TestATruncatedWriteNeverReachesDisk:
    """A short stream must be refused, not stored and warned about.

    Terraform does not fail an apply on a WARNING, so storing the partial bytes
    and returning one means the apply reports success over a truncated state
    file -- an aborted apply, a half-closed stream or a dropped chunk silently
    destroys good state.
    """

    async def test_good_state_survives_a_short_stream(self, backend: FileSystemStateStore) -> None:
        handler = ProviderHandler()
        await _write(handler, b"GOODSTATE-12")
        assert await backend.read_state(TYPE_NAME, STATE_ID) == b"GOODSTATE-12"

        response = await _write(handler, b"BAD01", declared=12)

        assert await backend.read_state(TYPE_NAME, STATE_ID) == b"GOODSTATE-12", (
            "a stream shorter than its declared total_length overwrote good state"
        )
        assert pb.Diagnostic.ERROR in _severities(response), (
            "a truncated write was reported as a warning, which Terraform does not fail on"
        )

    async def test_a_first_write_of_a_short_stream_stores_nothing(self, backend: FileSystemStateStore) -> None:
        handler = ProviderHandler()
        response = await _write(handler, b"BAD01", declared=12)

        assert pb.Diagnostic.ERROR in _severities(response)
        assert await backend.read_state(TYPE_NAME, STATE_ID) in (None, b"")

    async def test_a_matching_length_still_writes(self, backend: FileSystemStateStore) -> None:
        handler = ProviderHandler()
        response = await _write(handler, b"EXACTLY-OK")

        assert pb.Diagnostic.ERROR not in _severities(response)
        assert await backend.read_state(TYPE_NAME, STATE_ID) == b"EXACTLY-OK"

    async def test_an_undeclared_length_is_not_treated_as_a_mismatch(
        self, backend: FileSystemStateStore
    ) -> None:
        """total_length is optional; zero means "not declared", not "zero bytes"."""
        handler = ProviderHandler()
        response = await _write(handler, b"NO-DECLARED-LENGTH", declared=0)

        assert pb.Diagnostic.ERROR not in _severities(response)
        assert await backend.read_state(TYPE_NAME, STATE_ID) == b"NO-DECLARED-LENGTH"


class TestEveryReadChunkCarriesARange:
    """Core reads `chunk.Range.End` on every chunk without checking for nil.

    `grpc_provider.go` dereferences it, so a Response with no `range` panics the
    Terraform process and takes the diagnostic down with it.
    """

    async def test_the_error_path_sends_a_range(self, backend: FileSystemStateStore) -> None:
        async def _boom(*args: object, **kwargs: object) -> bytes:
            raise OSError("state directory is not readable")

        backend.read_state = _boom  # type: ignore[method-assign]

        handler = ProviderHandler()
        request = pb.ReadStateBytes.Request(type_name=TYPE_NAME, state_id=STATE_ID)
        responses = [response async for response in handler.ReadStateBytes(request, context=None)]

        assert responses, "the error path yielded nothing at all"
        for response in responses:
            assert response.HasField("range"), "a chunk without `range` panics Terraform on `chunk.Range.End`"

    async def test_the_empty_state_path_sends_a_range(self, backend: FileSystemStateStore) -> None:
        handler = ProviderHandler()
        request = pb.ReadStateBytes.Request(type_name=TYPE_NAME, state_id="never-written")
        responses = [response async for response in handler.ReadStateBytes(request, context=None)]

        assert responses
        for response in responses:
            assert response.HasField("range")

    async def test_the_ordinary_path_sends_a_range(self, backend: FileSystemStateStore) -> None:
        handler = ProviderHandler()
        await _write(handler, b"PAYLOAD")

        request = pb.ReadStateBytes.Request(type_name=TYPE_NAME, state_id=STATE_ID)
        responses = [response async for response in handler.ReadStateBytes(request, context=None)]

        assert responses
        for response in responses:
            assert response.HasField("range")


# 🌊🪢🔚
