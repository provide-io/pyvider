#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Minimal conftest for mutation testing - no autouse fixtures."""

import asyncio
from asyncio import AbstractEventLoop

import pytest


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """Create an instance of the default event loop for the session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# 🐍🏗️🔚
