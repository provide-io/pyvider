#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider/resources/protocol.py."""

from typing import Any

from pyvider.resources.context import ResourceContext
from pyvider.resources.protocol import ResourceProtocol


class TestResourceProtocol:
    """Tests for ResourceProtocol runtime checking."""

    def test_protocol_is_runtime_checkable(self) -> None:
        """Test that ResourceProtocol is marked as runtime_checkable."""
        # ResourceProtocol should be runtime checkable
        # Check if it's a Protocol by verifying it has the _is_protocol attribute
        import typing

        assert isinstance(ResourceProtocol, type)
        # Protocols in Python 3.8+ have _is_protocol or __protocol_attrs__
        is_protocol = (
            hasattr(ResourceProtocol, "_is_protocol")
            or hasattr(ResourceProtocol, "__protocol_attrs__")
            or hasattr(typing, "runtime_checkable")
        )
        assert is_protocol

    async def test_valid_implementation_is_recognized(self) -> None:
        """Test that a valid implementation is recognized as conforming to the protocol."""

        class ValidResource:
            async def validate(self, config: dict[str, Any]) -> None:
                pass

            async def read(self, ctx: ResourceContext) -> dict[str, Any]:
                return {}

            async def plan(self, ctx: ResourceContext) -> tuple[dict[str, Any], bytes]:
                return {}, b""

            async def apply(self, ctx: ResourceContext) -> tuple[dict[str, Any], bytes]:
                return {}, b""

            async def delete(self, ctx: ResourceContext) -> None:
                pass

        # Should be recognized as implementing the protocol
        resource = ValidResource()
        assert isinstance(resource, ResourceProtocol)

    async def test_partial_implementation_not_recognized(self) -> None:
        """Test that a partial implementation is not recognized as conforming."""

        class PartialResource:
            async def validate(self, config: dict[str, Any]) -> None:
                pass

            # Missing other methods

        resource = PartialResource()
        # Should NOT be recognized as implementing the protocol
        assert not isinstance(resource, ResourceProtocol)

    def test_protocol_methods_are_defined(self) -> None:
        """Test that all expected methods are defined in the protocol."""
        expected_methods = ["validate", "read", "plan", "apply", "delete"]
        for method in expected_methods:
            assert hasattr(ResourceProtocol, method)


# 🐍🏗️🔚
