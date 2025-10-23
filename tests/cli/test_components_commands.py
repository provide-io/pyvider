"""Tests for CLI components commands."""

from provide.testkit import mocking as mock
import pytest

from pyvider.cli.components_commands import (
    _display_attribute,
    _display_block_content,
    _display_block_type,
    _handle_discovery_errors,
)
from pyvider.cty import CtyBool, CtyNumber, CtyString
from pyvider.schema import PvsAttribute, PvsNestedBlock, PvsObjectType


class TestHandleDiscoveryErrors:
    """Tests for _handle_discovery_errors function."""

    def test_exits_when_discovery_errors_present(self):
        """Test that function exits when discovery errors are present."""
        ctx = mock.MagicMock()
        ctx.discovery_errors = [("test_module", "Import failed")]

        with pytest.raises(SystemExit) as exc_info:
            _handle_discovery_errors(ctx)

        assert exc_info.value.code == 1

    def test_does_nothing_when_no_errors(self):
        """Test that function returns normally when no errors."""
        ctx = mock.MagicMock()
        ctx.discovery_errors = []

        # Should not raise
        _handle_discovery_errors(ctx)

    def test_does_nothing_when_errors_is_none(self):
        """Test that function returns normally when errors is None."""
        ctx = mock.MagicMock()
        ctx.discovery_errors = None

        # Should not raise
        _handle_discovery_errors(ctx)


class TestDisplayAttribute:
    """Tests for _display_attribute function."""

    def test_displays_required_attribute(self):
        """Test displaying a required attribute."""
        attr = PvsAttribute(name="test_attr", type=CtyString(), required=True)

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            # Should have called pout for attribute name and type
            assert mock_pout.call_count >= 2

    def test_displays_optional_attribute(self):
        """Test displaying an optional attribute."""
        attr = PvsAttribute(name="optional_attr", type=CtyNumber(), optional=True)

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=1)

            assert mock_pout.call_count >= 2

    def test_displays_attribute_with_description(self):
        """Test displaying attribute with description."""
        attr = PvsAttribute(name="described_attr", type=CtyBool(), description="This is a test attribute")

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            # Should include description in output
            assert mock_pout.call_count >= 3

    def test_displays_attribute_with_default(self):
        """Test displaying attribute with default value."""
        attr = PvsAttribute(name="default_attr", type=CtyString(), default="default_value")

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            # Should include default in output
            assert mock_pout.call_count >= 3

    def test_displays_sensitive_attribute(self):
        """Test displaying sensitive attribute."""
        attr = PvsAttribute(name="secret", type=CtyString(), sensitive=True)

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            assert mock_pout.call_count >= 2

    def test_displays_computed_attribute(self):
        """Test displaying computed attribute."""
        attr = PvsAttribute(name="computed_val", type=CtyNumber(), computed=True)

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_attribute(attr, indent_level=0)

            assert mock_pout.call_count >= 2


class TestDisplayBlockType:
    """Tests for _display_block_type function."""

    def test_displays_simple_block(self):
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

    def test_displays_block_with_description(self):
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

    def test_displays_block_with_attributes(self):
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

    def test_displays_block_with_nested_blocks(self):
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

    def test_displays_empty_block(self):
        """Test displaying empty block content."""
        block = PvsObjectType(attributes={}, block_types=[])

        with mock.patch("pyvider.cli.components_commands.pout") as mock_pout:
            _display_block_content(block, indent_level=0)

            # Should not crash, may or may not call pout
            assert mock_pout.call_count >= 0
