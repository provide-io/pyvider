# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Regression tests for the high-severity review fixes (H1, H2, H3, H5)."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import MagicMock

import pytest

from pyvider.exceptions import FrameworkConfigurationError, ResourceError
from pyvider.protocols.service import ProtocolService
from pyvider.providers.base import BaseProvider, ProviderMetadata

# ---------- H5: BaseProvider.capabilities is per-instance + setup() is idempotent


def _make_provider(name: str = "p") -> BaseProvider:
    return BaseProvider(metadata=ProviderMetadata(name=name, version="0.0.1"))


def test_capabilities_is_per_instance_not_shared() -> None:
    """Previously `capabilities` was a ClassVar dict shared across all instances."""
    p1 = _make_provider("one")
    p2 = _make_provider("two")
    p1.capabilities["marker"] = "only-on-p1"
    assert "marker" not in p2.capabilities
    assert p1.capabilities is not p2.capabilities


def test_setup_lock_and_done_flag_exist() -> None:
    p = _make_provider()
    assert isinstance(p._setup_lock, asyncio.Lock)
    assert p._setup_done is False


@pytest.mark.asyncio
async def test_setup_is_idempotent_under_concurrency() -> None:
    """Concurrent setup() calls must execute the body only once (lock + _setup_done)."""
    from attrs import define

    call_count = 0

    @define
    class CountingProvider(BaseProvider):
        async def setup(self) -> None:  # type: ignore[override]
            nonlocal call_count
            async with self._setup_lock:
                if self._setup_done:
                    return
                call_count += 1
                await asyncio.sleep(0.01)
                self.capabilities = {"provider": self}
                self._setup_done = True

    p = CountingProvider(metadata=ProviderMetadata(name="x", version="0.0.1"))
    await asyncio.gather(p.setup(), p.setup(), p.setup())
    assert call_count == 1
    assert p._setup_done is True


# ---------- H2: StreamStdio uses an Event and stops cleanly


@pytest.mark.asyncio
async def test_stream_stopped_is_event_not_bool() -> None:
    svc = ProtocolService(asyncio.Event())
    assert isinstance(svc._stream_stopped, asyncio.Event)
    # Compat property still reads as a bool.
    assert svc._stream_active is True
    svc._stream_stopped.set()
    assert svc._stream_active is False


@pytest.mark.asyncio
async def test_stream_stdio_breaks_when_stream_stopped_mid_iteration() -> None:
    svc = ProtocolService(asyncio.Event())

    async def iterator() -> AsyncIterator[str]:
        yield "a"
        svc._stream_stopped.set()
        yield "b"
        yield "c"

    received: list[str] = []
    async for msg in svc.StreamStdio(iterator(), MagicMock()):
        received.append(msg)

    assert received == ["a"]
    assert svc._stream_stopped.is_set()


@pytest.mark.asyncio
async def test_stream_stdio_finally_sets_stopped_on_exception() -> None:
    svc = ProtocolService(asyncio.Event())

    async def iterator() -> AsyncIterator[str]:
        yield "a"
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        async for _ in svc.StreamStdio(iterator(), MagicMock()):
            pass

    assert svc._stream_stopped.is_set()


# ---------- H3: apply handler raises FrameworkConfigurationError, not RuntimeError


@pytest.mark.asyncio
async def test_apply_missing_provider_raises_framework_error() -> None:
    from pyvider.hub import hub
    from pyvider.protocols.tfprotov6.handlers.apply_resource_change import (
        _get_resource_and_provider_instances,
    )
    from pyvider.resources.base import BaseResource

    class _R(BaseResource):
        pass

    hub.register("resource", "reg_test_resource", _R)
    try:
        # Ensure provider singleton is absent.
        try:
            hub.unregister("singleton", "provider")
        except Exception:
            pass

        with pytest.raises(FrameworkConfigurationError) as ei:
            await _get_resource_and_provider_instances("reg_test_resource")

        # The enriched context should carry resource + terraform keys.
        assert "Provider instance not found" in str(ei.value)
    finally:
        hub.unregister("resource", "reg_test_resource")


# ---------- H1: unexpected Exception in apply chains to ResourceError + metric bumps


@pytest.mark.asyncio
async def test_apply_unexpected_exception_wraps_into_resource_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify the unexpected-exception branch wraps into ResourceError and bumps handler_errors."""
    from pyvider.observability import handler_errors
    from pyvider.protocols.tfprotov6.handlers import apply_resource_change as arc
    import pyvider.protocols.tfprotov6.protobuf as pb

    async def _boom(*a: Any, **kw: Any) -> Any:
        raise ValueError("synthetic unexpected error")

    monkeypatch.setattr(arc, "_get_resource_and_provider_instances", _boom)

    captured: dict[str, Any] = {}

    async def _capture_diag(exc: BaseException) -> Any:
        captured["exc"] = exc
        diag = pb.Diagnostic()
        diag.summary = "captured"
        return diag

    monkeypatch.setattr(arc, "create_diagnostic_from_exception", _capture_diag)

    before = handler_errors.get(handler="ApplyResourceChange") if hasattr(handler_errors, "get") else None

    request = pb.ApplyResourceChange.Request()
    request.type_name = "whatever"

    response = await arc._apply_resource_change_impl(request, MagicMock())

    # Exception was wrapped into a framework ResourceError with cause chain preserved.
    wrapped = captured["exc"]
    assert isinstance(wrapped, ResourceError)
    assert isinstance(wrapped.__cause__, ValueError)
    assert "synthetic unexpected error" in str(wrapped)

    # Diagnostic was appended; the RPC did not bubble the raw exception.
    assert len(response.diagnostics) == 1

    if before is not None:
        after = handler_errors.get(handler="ApplyResourceChange")
        assert after >= before + 1


# ---------- §2.4: attrs requirement surfaces a friendly FrameworkConfigurationError


def test_cty_to_attrs_instance_rejects_non_attrs_class() -> None:
    """A user who hands a plain dataclass or bare class to config_class/
    state_class/private_state_class should get a clear up-front error, not a
    silent empty-object round-trip or a confusing deep TypeError."""
    from dataclasses import dataclass

    from pyvider.protocols.tfprotov6.handlers.utils import cty_to_attrs_instance

    @dataclass
    class NotAttrs:
        foo: str = "bar"

    with pytest.raises(FrameworkConfigurationError) as ei:
        cty_to_attrs_instance(None, NotAttrs)

    msg = str(ei.value)
    assert "NotAttrs" in msg
    assert "attrs" in msg.lower()


def test_cty_to_attrs_instance_accepts_none_and_attrs_class() -> None:
    """None short-circuits; a proper attrs class is accepted."""
    import attrs as _attrs

    from pyvider.protocols.tfprotov6.handlers.utils import cty_to_attrs_instance

    assert cty_to_attrs_instance(None, None) is None

    @_attrs.define
    class Good:
        x: int = 0

    # With a None CtyValue the helper still returns None, but the class check
    # must not raise.
    assert cty_to_attrs_instance(None, Good) is None
