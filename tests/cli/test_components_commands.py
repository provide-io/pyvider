#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI components commands."""

from click.testing import CliRunner
from provide.testkit import mocking as mock
import pytest

from pyvider.cli.components_commands import (
    _display_attribute,
    _display_block_content,
    _display_block_type,
    _handle_discovery_errors,
    show_diagnostics,
)
from pyvider.cty import CtyBool, CtyNumber, CtyString
from pyvider.schema import PvsAttribute, PvsNestedBlock, PvsObjectType


class TestHandleDiscoveryErrors:
    """Tests for _handle_discovery_errors function."""

    def test_exits_when_discovery_errors_present(self) -> None:
        """Test that function exits when discovery errors are present."""
        ctx = mock.MagicMock()
        ctx.discovery_errors = [("test_module", "Import failed")]

        with pytest.raises(SystemExit) as exc_info:
            _handle_discovery_errors(ctx)

        assert exc_info.value.code == 1

    def test_does_nothing_when_no_errors(self) -> None:
        """Test that function returns normally when no errors."""
        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        # Should not raise
        _handle_discovery_errors(ctx)

    def test_does_nothing_when_errors_is_none(self) -> None:
        """Test that function returns normally when errors is None."""
        ctx = mock.MagicMock()
        ctx.discovery_errors = None

        # Should not raise
        _handle_discovery_errors(ctx)


class TestDisplayAttribute:
    """Tests for _display_attribute function."""

    def test_displays_required_attribute(self) -> None:
        """Test displaying a required attribute."""
        attr = PvsAttribute(name="test_attr", type=CtyString(), required=True)

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            # Should have called pout for attribute name and type
            assert mock_pout.call_count >= 2

    def test_displays_optional_attribute(self) -> None:
        """Test displaying an optional attribute."""
        attr = PvsAttribute(name="optional_attr", type=CtyNumber(), optional=True)

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=1)

            assert mock_pout.call_count >= 2

    def test_displays_attribute_with_description(self) -> None:
        """Test displaying attribute with description."""
        attr = PvsAttribute(name="described_attr", type=CtyBool(), description="This is a test attribute")

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            # Should include description in output
            assert mock_pout.call_count >= 3

    def test_displays_attribute_with_default(self) -> None:
        """Test displaying attribute with default value."""
        attr = PvsAttribute(name="default_attr", type=CtyString(), default="default_value")

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            # Should include default in output
            assert mock_pout.call_count >= 3

    def test_displays_sensitive_attribute(self) -> None:
        """Test displaying sensitive attribute."""
        attr = PvsAttribute(name="secret", type=CtyString(), sensitive=True)

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            assert mock_pout.call_count >= 2

    def test_displays_computed_attribute(self) -> None:
        """Test displaying computed attribute."""
        attr = PvsAttribute(name="computed_val", type=CtyNumber(), computed=True)

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            assert mock_pout.call_count >= 2


class TestDisplayBlockType:
    """Tests for _display_block_type function."""

    def test_displays_simple_block(self) -> None:
        """Test displaying a simple block type."""
        block_content = PvsObjectType(attributes={"name": PvsAttribute(name="name", type=CtyString())})
        # Create a mock block with nesting attribute
        block = mock.MagicMock(spec=PvsNestedBlock)
        block.type_name = "test_block"
        block.nesting = mock.MagicMock()
        block.nesting.name = "SINGLE"
        block.block = block_content
        block.description = None

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_block_type(block, indent_level=0)

            # Should have output for block name and attributes
            assert mock_pout.call_count >= 2

    def test_displays_block_with_description(self) -> None:
        """Test displaying block with description."""
        block_content = PvsObjectType(attributes={})
        block = mock.MagicMock(spec=PvsNestedBlock)
        block.type_name = "described_block"
        block.nesting = mock.MagicMock()
        block.nesting.name = "LIST"
        block.block = block_content
        block.description = "Test block description"

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_block_type(block, indent_level=0)

            assert mock_pout.call_count >= 2


class TestDisplayBlockContent:
    """Tests for _display_block_content function."""

    def test_displays_block_with_attributes(self) -> None:
        """Test displaying block content with attributes."""
        block = PvsObjectType(
            attributes={
                "attr1": PvsAttribute(name="attr1", type=CtyString()),
                "attr2": PvsAttribute(name="attr2", type=CtyNumber()),
            }
        )

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_block_content(block, indent_level=0)

            # Should display both attributes
            assert mock_pout.call_count >= 4

    def test_displays_block_with_nested_blocks(self) -> None:
        """Test displaying block content with nested blocks."""
        nested_content = PvsObjectType(attributes={"inner": PvsAttribute(name="inner", type=CtyString())})
        nested_block = mock.MagicMock(spec=PvsNestedBlock)
        nested_block.type_name = "nested"
        nested_block.nesting = mock.MagicMock()
        nested_block.nesting.name = "SINGLE"
        nested_block.block = nested_content
        nested_block.description = None

        block = PvsObjectType(attributes={}, block_types=[nested_block])

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_block_content(block, indent_level=0)

            # Should display nested block
            assert mock_pout.call_count >= 1

    def test_displays_empty_block(self) -> None:
        """Test displaying empty block content."""
        block = PvsObjectType(attributes={}, block_types=[])

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_block_content(block, indent_level=0)

            # Should not crash, may or may not call pout
            assert mock_pout.call_count >= 0


class TestShowDiagnosticsCommand:
    """Comprehensive tests for show_diagnostics command."""

    def test_shows_diagnostics_successfully(self) -> None:
        """Test that diagnostics displays successfully with valid data."""
        mock_diagnostics = {
            "total_component_types": 3,
            "total_components": 10,
            "component_breakdown": {
                "provider": 1,
                "data_source": 5,
                "resource": 4,
            },
        }

        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        with (
            mock.patch("pyvider.cli.components_commands.get_hub_diagnostics", return_value=mock_diagnostics),
            mock.patch("pyvider.cli.components_commands.pout") as mock_pout,
        ):
            runner = CliRunner()
            result = runner.invoke(show_diagnostics, obj=ctx, catch_exceptions=False)

            assert result.exit_code == 0
            # Verify pout was called with diagnostics info
            assert mock_pout.call_count > 0

    def test_shows_diagnostics_with_timing(self) -> None:
        """Test that diagnostics includes timing information."""
        mock_diagnostics = {
            "total_component_types": 2,
            "total_components": 5,
            "component_breakdown": {
                "provider": 1,
                "data_source": 4,
            },
        }

        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        with (
            mock.patch("pyvider.cli.components_commands.get_hub_diagnostics", return_value=mock_diagnostics),
            mock.patch("pyvider.cli.components_commands.pout") as mock_pout,
        ):
            runner = CliRunner()
            result = runner.invoke(show_diagnostics, obj=ctx, catch_exceptions=False)

            assert result.exit_code == 0
            # Check that timing was displayed
            timing_calls = [call for call in mock_pout.call_args_list if "Discovery time" in str(call)]
            assert len(timing_calls) > 0

    def test_shows_diagnostics_with_empty_components(self) -> None:
        """Test diagnostics display when no components are found."""
        mock_diagnostics = {
            "total_component_types": 0,
            "total_components": 0,
            "component_breakdown": {},
        }

        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        with (
            mock.patch("pyvider.cli.components_commands.get_hub_diagnostics", return_value=mock_diagnostics),
            mock.patch("pyvider.cli.components_commands.pout") as mock_pout,
        ):
            runner = CliRunner()
            result = runner.invoke(show_diagnostics, obj=ctx, catch_exceptions=False)

            assert result.exit_code == 0
            assert mock_pout.call_count > 0

    def test_shows_diagnostics_handles_exceptions(self) -> None:
        """Test that diagnostics command handles exceptions gracefully."""
        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        with (
            mock.patch(
                "pyvider.cli.components_commands.get_hub_diagnostics",
                side_effect=RuntimeError("Test error"),
            ),
            mock.patch("pyvider.cli.components_commands.perr") as mock_perr,
        ):
            runner = CliRunner()
            result = runner.invoke(show_diagnostics, obj=ctx, catch_exceptions=False)

            # Should not crash, should display error
            assert result.exit_code == 0
            error_calls = [
                call for call in mock_perr.call_args_list if "Failed to get diagnostics" in str(call)
            ]
            assert len(error_calls) > 0

    def test_shows_diagnostics_displays_all_component_types(self) -> None:
        """Test that all component types in breakdown are displayed."""
        mock_diagnostics = {
            "total_component_types": 4,
            "total_components": 15,
            "component_breakdown": {
                "provider": 1,
                "data_source": 8,
                "resource": 5,
                "function": 1,
            },
        }

        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        with (
            mock.patch("pyvider.cli.components_commands.get_hub_diagnostics", return_value=mock_diagnostics),
            mock.patch("pyvider.cli.components_commands.pout"),
            mock.patch("pyvider.cli.components_commands.format_table") as mock_format_table,
        ):
            runner = CliRunner()
            result = runner.invoke(show_diagnostics, obj=ctx, catch_exceptions=False)

            assert result.exit_code == 0
            # Verify format_table was called
            assert mock_format_table.call_count > 0

    def test_timing_uses_perf_counter(self) -> None:
        """Test that timing uses time.perf_counter() instead of timed_block()."""
        mock_diagnostics = {
            "total_component_types": 1,
            "total_components": 1,
            "component_breakdown": {"provider": 1},
        }

        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        with (
            mock.patch("pyvider.cli.components_commands.get_hub_diagnostics", return_value=mock_diagnostics),
            mock.patch("pyvider.cli.components_commands.pout"),
            mock.patch("pyvider.cli.components_commands.time") as mock_time,
        ):
            mock_time.perf_counter.side_effect = [0.0, 0.123]  # start, end

            runner = CliRunner()
            result = runner.invoke(show_diagnostics, obj=ctx, catch_exceptions=False)

            assert result.exit_code == 0
            # Verify perf_counter was called twice (start and end)
            assert mock_time.perf_counter.call_count == 2

    def test_diagnostics_displays_correct_summary_stats(self) -> None:
        """Test that summary statistics are correctly displayed."""
        mock_diagnostics = {
            "total_component_types": 3,
            "total_components": 12,
            "component_breakdown": {
                "provider": 2,
                "data_source": 7,
                "resource": 3,
            },
        }

        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        with (
            mock.patch("pyvider.cli.components_commands.get_hub_diagnostics", return_value=mock_diagnostics),
            mock.patch("pyvider.cli.components_commands.pout") as mock_pout,
        ):
            runner = CliRunner()
            result = runner.invoke(show_diagnostics, obj=ctx, catch_exceptions=False)

            assert result.exit_code == 0
            # Check that total_component_types and total_components were displayed
            all_calls = "".join(str(call) for call in mock_pout.call_args_list)
            assert "3" in all_calls  # total_component_types
            assert "12" in all_calls  # total_components


# 🐍🏗️🔚
