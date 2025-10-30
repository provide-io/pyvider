#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum


class ResourceState(Enum):
    """Resource lifecycle states."""

    UNKNOWN = "UNKNOWN"
    PLANNED = "PLANNED"
    CREATING = "CREATING"
    CREATED = "CREATED"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    DELETED = "DELETED"
    FAILED = "FAILED"


@dataclass
class ResourceLifecycle:
    """Tracks resource lifecycle state."""

    state: ResourceState = ResourceState.UNKNOWN
    last_operation: str | None = None
    last_updated: datetime | None = None
    error: str | None = None

    def transition_to(self, state: ResourceState, operation: str) -> None:
        """Transition to a new state."""
        self.state = state
        self.last_operation = operation
        self.last_updated = datetime.now(UTC)


# 🐍🏗️🔚
