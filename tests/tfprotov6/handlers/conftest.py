#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Shared fixtures for tfprotov6 handler tests."""

from collections.abc import Iterator

from provide.testkit.mocking import MagicMock
import pytest

import pyvider.protocols.tfprotov6.protobuf as pb


@pytest.fixture
def sample_request() -> pb.GetProviderSchema.Request:
    """Create a sample GetProviderSchema request."""
    return pb.GetProviderSchema.Request()


@pytest.fixture
def mock_provider_instance() -> MagicMock:
    """Create a mock provider instance."""
    mock_provider = MagicMock()
    mock_provider.schema = MagicMock()
    return mock_provider


@pytest.fixture
def mock_resource_class() -> MagicMock:
    """Create a mock resource class."""
    mock_class = MagicMock()
    mock_schema = MagicMock()
    mock_class.get_schema.return_value = mock_schema
    mock_class._is_test_only = False  # Needed for get_filtered_components
    return mock_class


@pytest.fixture
def clear_schema_cache() -> Iterator[None]:
    """Clear the schema cache before each test."""
    import pyvider.protocols.tfprotov6.handlers.get_provider_schema as module

    module._schema_future = None
    module._task = None
    yield
    module._schema_future = None
    module._task = None
