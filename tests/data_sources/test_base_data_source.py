#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for data sources base module."""

import pytest

from pyvider.common.context import BaseContext
from pyvider.data_sources.base import BaseDataSource
from pyvider.protocols.tfprotov6.protobuf import Diagnostic
from pyvider.schema import PvsSchema, a_num, a_str, s_data_source


class TestDataSource(BaseDataSource):
    """Concrete test data source for testing."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source(
            attributes={
                "name": a_str(required=True),
                "count": a_num(optional=True),
            }
        )

    async def _validate_config(self, config: dict) -> list[Diagnostic]:
        """Validate configuration."""
        return []

    async def read(self, ctx: BaseContext) -> dict:
        """Simple read implementation."""
        return {"name": "test", "count": 42}


class TestBaseDataSource:
    """Tests for BaseDataSource class."""

    def test_data_source_has_get_schema(self) -> None:
        """Test that data source has get_schema method."""
        assert hasattr(TestDataSource, "get_schema")
        schema = TestDataSource.get_schema()
        assert schema is not None

    def test_data_source_has_read_method(self) -> None:
        """Test that data source has read method."""
        ds = TestDataSource()
        assert hasattr(ds, "read")
        assert callable(ds.read)

    @pytest.mark.asyncio
    async def test_data_source_read_returns_data(self) -> None:
        """Test that read method returns data."""
        ds = TestDataSource()
        result = await ds.read(None)
        assert result == {"name": "test", "count": 42}

    def test_data_source_schema_structure(self) -> None:
        """Test the structure of the data source schema."""
        schema = TestDataSource.get_schema()
        assert schema is not None
        # Schema should have a block attribute
        assert hasattr(schema, "block")


class TestDataSourceEdgeCases:
    """Edge case tests for data sources."""

    def test_data_source_without_implementation_fails(self) -> None:
        """Test that abstract methods must be implemented."""

        # Incomplete data source missing required methods
        class IncompleteDataSource(BaseDataSource):
            @classmethod
            def get_schema(cls) -> PvsSchema:
                return s_data_source(attributes={"id": a_str()})

            # Missing read and _validate_config methods

        # Should not be able to instantiate
        with pytest.raises(TypeError, match="abstract"):
            IncompleteDataSource()

    @pytest.mark.asyncio
    async def test_data_source_with_none_context(self) -> None:
        """Test data source with None context."""
        ds = TestDataSource()
        result = await ds.read(None)
        assert result is not None

    def test_multiple_data_source_instances(self) -> None:
        """Test creating multiple instances of the same data source."""
        ds1 = TestDataSource()
        ds2 = TestDataSource()
        assert ds1 is not ds2
        assert isinstance(ds1, type(ds2))

    @pytest.mark.asyncio
    async def test_validate_with_none_config(self) -> None:
        """Test validate method with None config returns empty list."""
        ds = TestDataSource()
        result = await ds.validate(None)
        assert result == []

    @pytest.mark.asyncio
    async def test_validate_with_valid_config(self) -> None:
        """Test validate method with valid config."""
        ds = TestDataSource()
        config = {"name": "test", "count": 5}
        result = await ds.validate(config)
        assert result == []

    def test_from_cty_delegates_to_base_resource(self) -> None:
        """Test that from_cty delegates to BaseResource.from_cty."""
        # This tests the from_cty class method exists and is callable
        assert hasattr(TestDataSource, "from_cty")
        assert callable(TestDataSource.from_cty)


# 🐍🏗️🔚
