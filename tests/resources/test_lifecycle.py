#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from datetime import UTC, datetime

from pyvider.resources.lifecycle import (
    ResourceLifecycle,
    ResourceState,
)


def test_resource_state_enum() -> None:
    assert ResourceState.UNKNOWN.value == "UNKNOWN"
    assert ResourceState.PLANNED.value == "PLANNED"
    assert ResourceState.CREATING.value == "CREATING"
    assert ResourceState.CREATED.value == "CREATED"
    assert ResourceState.UPDATING.value == "UPDATING"
    assert ResourceState.DELETING.value == "DELETING"
    assert ResourceState.DELETED.value == "DELETED"
    assert ResourceState.FAILED.value == "FAILED"


def test_resource_lifecycle_init() -> None:
    lifecycle = ResourceLifecycle()
    assert lifecycle.state == ResourceState.UNKNOWN
    assert lifecycle.last_operation is None
    assert lifecycle.last_updated is None
    assert lifecycle.error is None


def test_resource_lifecycle_transition_to() -> None:
    lifecycle = ResourceLifecycle()
    before = datetime.now(UTC)
    lifecycle.transition_to(ResourceState.CREATED, "create")
    after = datetime.now(UTC)

    assert lifecycle.state == ResourceState.CREATED
    assert lifecycle.last_operation == "create"
    assert lifecycle.last_updated is not None
    assert before <= lifecycle.last_updated <= after


# 🐍🏗️🔚
