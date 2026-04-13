#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Mutation tests for upgrade_resource_state handler."""

import json
from pathlib import Path
import sys

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from pyvider.protocols.tfprotov6.handlers.upgrade_resource_state import (
    UpgradeResourceStateHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.mark.asyncio
async def test_passes_through_json_state() -> None:
    """State should be returned unchanged."""
    state_data = {"name": "test", "value": 123}
    state_json = json.dumps(state_data).encode("utf-8")

    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
        raw_state=pb.RawState(json=state_json),
    )

    response = await UpgradeResourceStateHandler(request, context=None)

    assert response.upgraded_state.json == state_json
    assert len(response.diagnostics) == 0


@pytest.mark.asyncio
async def test_handles_empty_state() -> None:
    """Empty state should return empty object."""
    request = pb.UpgradeResourceState.Request(
        type_name="test_resource",
        version=0,
        raw_state=pb.RawState(),
    )

    response = await UpgradeResourceStateHandler(request, context=None)

    assert response.upgraded_state.json == b"{}"
    assert len(response.diagnostics) == 0


# 🐍🏗️🔚
