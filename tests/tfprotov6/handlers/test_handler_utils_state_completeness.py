#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for handlers/utils.py::complete_state_dict.

Regression coverage for provide-io/pyvider#50 (write-only nulling must be
unconditional) and its follow-up: any other schema attribute missing from a
resource's returned state is a resource implementation bug, and should raise
a clear pyvider-level error rather than surface as cty's generic one.
"""

import pytest

from pyvider.exceptions import IncompleteResourceStateError
from pyvider.protocols.tfprotov6.handlers.utils import complete_state_dict
from pyvider.schema import a_str, s_resource

SCHEMA = s_resource(
    {
        "id": a_str(computed=True),
        "name": a_str(required=True),
        "secret": a_str(required=True, write_only=True),
    }
)


def test_write_only_forced_null_when_present() -> None:
    raw = {"id": "1", "name": "n", "secret": "leaked-value"}

    result = complete_state_dict(raw, SCHEMA.block, resource_type="demo", state_class_name="DemoState")

    assert result["secret"] is None


def test_write_only_forced_null_when_absent() -> None:
    raw = {"id": "1", "name": "n"}

    result = complete_state_dict(raw, SCHEMA.block, resource_type="demo", state_class_name="DemoState")

    assert result["secret"] is None


def test_non_write_only_attribute_left_alone() -> None:
    raw = {"id": "1", "name": "n", "secret": None}

    result = complete_state_dict(raw, SCHEMA.block, resource_type="demo", state_class_name="DemoState")

    assert result["name"] == "n"
    assert result["id"] == "1"


def test_missing_non_write_only_attribute_raises() -> None:
    raw = {"id": "1", "secret": None}

    with pytest.raises(IncompleteResourceStateError, match="'name'") as exc_info:
        complete_state_dict(raw, SCHEMA.block, resource_type="demo", state_class_name="DemoState")

    message = str(exc_info.value)
    assert "demo" in message
    assert "DemoState" in message
