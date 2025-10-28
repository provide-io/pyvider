#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for data sources base module."""

import pytest

from pyvider.data_sources.base import BaseDataSource
from pyvider.schema import a_num, a_str, s_data_source


class TestDataSource(BaseDataSource):
    """Concrete test data source for testing."""

    @classmethod
    def get_schema(cls):
        return s_data_source(
            attributes={
                "name": a_str(required=True),
                "count": a_num(optional=True),
            }
        )

    async def _validate_config(self, config):
        """Validate configuration."""
        return []

    async def read(self, ctx):
        """Simple read implementation."""
        return {"name": "test", "count": 42}


class TestBaseDataSource:
    """Tests for BaseDataSource class."""

    def test_data_source_has_get_schema(self):
        """Test that data source has get_schema method."""
        assert hasattr(TestDataSource, "get_schema")
        schema = TestDataSource.get_schema()
        assert schema is not None

    def test_data_source_has_read_method(self):
        """Test that data source has read method."""
        ds = TestDataSource()
        assert hasattr(ds, "read")
        assert callable(ds.read)

    @pytest.mark.asyncio
    async def test_data_source_read_returns_data(self):
        """Test that read method returns data."""
        ds = TestDataSource()
        result = await ds.read(None)
        assert result == {"name": "test", "count": 42}

    def test_data_source_schema_structure(self):
        """Test the structure of the data source schema."""
        schema = TestDataSource.get_schema()
        assert schema is not None
        # Schema should have a block attribute
        assert hasattr(schema, "block")


class TestDataSourceEdgeCases:
    """Edge case tests for data sources."""

    def test_data_source_without_implementation_fails(self):
        """Test that abstract methods must be implemented."""

        # Incomplete data source missing required methods
        class IncompleteDataSource(BaseDataSource):
            @classmethod
            def get_schema(cls):
                return s_data_source(attributes={"id": a_str()})

            # Missing read and _validate_config methods

        # Should not be able to instantiate
        with pytest.raises(TypeError, match="abstract"):
            IncompleteDataSource()

    @pytest.mark.asyncio
    async def test_data_source_with_none_context(self):
        """Test data source with None context."""
        ds = TestDataSource()
        result = await ds.read(None)
        assert result is not None

    def test_multiple_data_source_instances(self):
        """Test creating multiple instances of the same data source."""
        ds1 = TestDataSource()
        ds2 = TestDataSource()
        assert ds1 is not ds2
        assert type(ds1) == type(ds2)

    @pytest.mark.asyncio
    async def test_validate_with_none_config(self):
        """Test validate method with None config returns empty list."""
        ds = TestDataSource()
        result = await ds.validate(None)
        assert result == []

    @pytest.mark.asyncio
    async def test_validate_with_valid_config(self):
        """Test validate method with valid config."""
        ds = TestDataSource()
        config = {"name": "test", "count": 5}
        result = await ds.validate(config)
        assert result == []

    def test_from_cty_delegates_to_base_resource(self):
        """Test that from_cty delegates to BaseResource.from_cty."""
        # This tests the from_cty class method exists and is callable
        assert hasattr(TestDataSource, "from_cty")
        assert callable(TestDataSource.from_cty)

# 🐍🏗️🔚
