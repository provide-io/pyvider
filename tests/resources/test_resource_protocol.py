#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for resource protocol and type aliases."""

from typing import Any

from pyvider.resources.base import ResourceContext
from pyvider.resources.protocol import ResourceProtocol
from pyvider.resources.types import ResourceId, ResourceName, ResourceType


class _DummyResource:
    async def validate(self, config: dict[str, Any]) -> None:
        return None

    async def read(self, ctx: ResourceContext) -> dict[str, Any]:
        return {"state": "ok"}

    async def plan(self, ctx: ResourceContext) -> tuple[dict[str, Any], bytes]:
        return {"state": "planned"}, b"plan"

    async def apply(self, ctx: ResourceContext) -> tuple[dict[str, Any], bytes]:
        return {"state": "applied"}, b"apply"

    async def delete(self, ctx: ResourceContext) -> None:
        return None


def test_resource_protocol_runtime_checkable() -> None:
    """A concrete resource implementation should satisfy the runtime protocol check."""
    dummy = _DummyResource()
    assert isinstance(dummy, ResourceProtocol)


def test_resource_type_aliases() -> None:
    """Resource-specific aliases should resolve to the expected base types."""
    assert ResourceName("home") == "home"
    assert ResourceId("abc123") == "abc123"
    assert getattr(ResourceType, "__name__", "") == "ResourceType"


# 🐍🏗️🔚
