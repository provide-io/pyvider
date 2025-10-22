"""Additional tests for components_commands module (for coverage improvement)."""

from unittest import mock

from click.testing import CliRunner
import pytest

from pyvider.cli import cli


class TestComponentsGroup:
    """Tests for components command group."""

    def test_components_group_exists(self):
        """Test that components group is registered."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "components" in result.output

    def test_components_help_shows_subcommands(self):
        """Test that components help shows subcommands."""
        runner = CliRunner()
        result = runner.invoke(cli, ["components", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "show" in result.output


class TestComponentsListCommand:
    """Tests for components list command."""

    @mock.patch("pyvider.cli.components_commands.registry")
    def test_list_shows_no_components_message(self, mock_registry):
        """Test that list shows message when no components found."""
        mock_registry.list_components.return_value = {
            "provider": {},
            "resource": {},
            "data_source": {},
        }

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "list"])
        assert "No components found" in result.output

    @mock.patch("pyvider.cli.components_commands.registry")
    def test_list_shows_available_components(self, mock_registry):
        """Test that list shows available components."""
        mock_registry.list_components.return_value = {
            "provider": {"my_provider": mock.MagicMock()},
            "resource": {"my_resource": mock.MagicMock()},
            "data_source": {},
        }

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "list"])
        assert result.exit_code == 0
        assert "my_provider" in result.output
        assert "my_resource" in result.output


class TestComponentsShowCommand:
    """Tests for components show command."""

    @mock.patch("pyvider.cli.components_commands.registry")
    def test_show_requires_component_type(self, mock_registry):
        """Test that show requires component type argument."""
        runner = CliRunner()
        result = runner.invoke(cli, ["components", "show"])
        assert result.exit_code != 0

    @mock.patch("pyvider.cli.components_commands.registry")
    def test_show_requires_component_name(self, mock_registry):
        """Test that show requires component name argument."""
        runner = CliRunner()
        result = runner.invoke(cli, ["components", "show", "resource"])
        assert result.exit_code != 0

    @mock.patch("pyvider.cli.components_commands.registry")
    def test_show_handles_not_found_component(self, mock_registry):
        """Test that show handles component not found gracefully."""
        mock_registry.get_component.return_value = None

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "show", "resource", "nonexistent"])
        assert "not found" in result.output.lower()

    @mock.patch("pyvider.cli.components_commands.registry")
    def test_show_handles_component_without_schema(self, mock_registry):
        """Test that show handles components without schema."""
        mock_component = mock.MagicMock()
        del mock_component.get_schema  # Remove get_schema method
        del mock_component.schema  # Remove schema attribute
        mock_registry.get_component.return_value = mock_component

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "show", "resource", "test"])
        # Should handle gracefully
        assert result.exit_code == 0 or "schema" in result.output.lower()


class TestComponentsDiagnosticsCommand:
    """Tests for components diagnostics command."""

    @mock.patch("pyvider.cli.components_commands.get_hub_diagnostics")
    def test_diagnostics_shows_summary(self, mock_get_diagnostics):
        """Test that diagnostics shows summary information."""
        mock_get_diagnostics.return_value = {
            "total_component_types": 5,
            "total_components": 10,
            "component_breakdown": {
                "resource": 4,
                "data_source": 3,
                "provider": 1,
            }
        }

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "diagnostics"])
        assert result.exit_code == 0
        assert "Hub Diagnostics" in result.output
        assert "Total component types: 5" in result.output
        assert "Total components: 10" in result.output

    @mock.patch("pyvider.cli.components_commands.get_hub_diagnostics")
    def test_diagnostics_shows_component_breakdown(self, mock_get_diagnostics):
        """Test that diagnostics shows component breakdown."""
        mock_get_diagnostics.return_value = {
            "total_component_types": 2,
            "total_components": 5,
            "component_breakdown": {
                "resource": 3,
                "data_source": 2,
            }
        }

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "diagnostics"])
        assert result.exit_code == 0
        assert "Component Breakdown" in result.output or "Components by Type" in result.output

    @mock.patch("pyvider.cli.components_commands.get_hub_diagnostics")
    def test_diagnostics_handles_empty_breakdown(self, mock_get_diagnostics):
        """Test that diagnostics handles empty component breakdown."""
        mock_get_diagnostics.return_value = {
            "total_component_types": 0,
            "total_components": 0,
            "component_breakdown": {}
        }

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "diagnostics"])
        assert result.exit_code == 0
        assert "No components discovered" in result.output or "0" in result.output

    @mock.patch("pyvider.cli.components_commands.get_hub_diagnostics")
    def test_diagnostics_handles_exception(self, mock_get_diagnostics):
        """Test that diagnostics handles exceptions gracefully."""
        mock_get_diagnostics.side_effect = RuntimeError("Hub error")

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "diagnostics"])
        assert "Failed" in result.output or result.exit_code != 0


class TestHandleDiscoveryErrors:
    """Tests for _handle_discovery_errors function."""

    @mock.patch("sys.exit")
    def test_handle_discovery_errors_exits_on_errors(self, mock_exit):
        """Test that _handle_discovery_errors exits when errors present."""
        from pyvider.cli.context import PyviderContext
        from pyvider.cli.components_commands import _handle_discovery_errors

        ctx = PyviderContext()
        ctx.discovery_errors = [("test_module", ImportError("test error"))]

        _handle_discovery_errors(ctx)

        # Should have called sys.exit(1)
        mock_exit.assert_called_once_with(1)

    def test_handle_discovery_errors_no_exit_on_no_errors(self):
        """Test that _handle_discovery_errors doesn't exit without errors."""
        from pyvider.cli.context import PyviderContext
        from pyvider.cli.components_commands import _handle_discovery_errors

        ctx = PyviderContext()
        ctx.discovery_errors = []

        # Should not raise or exit
        _handle_discovery_errors(ctx)  # Should complete normally


class TestSchemaDisplay:
    """Tests for schema display functions."""

    @mock.patch("pyvider.cli.components_commands.registry")
    def test_show_displays_attribute_details(self, mock_registry):
        """Test that show displays attribute details."""
        from pyvider.schema import s_resource, a_str

        mock_component = mock.MagicMock()
        mock_component.get_schema.return_value = s_resource(
            attributes={"name": a_str(required=True, description="Resource name")}
        )
        mock_registry.get_component.return_value = mock_component

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "show", "resource", "test"])
        assert result.exit_code == 0
        # Should show attribute info
        assert "name" in result.output or "Attribute" in result.output

    @mock.patch("pyvider.cli.components_commands.registry")
    def test_show_displays_nested_blocks(self, mock_registry):
        """Test that show displays nested blocks."""
        from pyvider.schema import s_resource, a_str, b_single

        mock_component = mock.MagicMock()
        mock_component.get_schema.return_value = s_resource(
            attributes={"id": a_str()},
            blocks=[b_single("config", attributes={"value": a_str()})]
        )
        mock_registry.get_component.return_value = mock_component

        runner = CliRunner()
        result = runner.invoke(cli, ["components", "show", "resource", "test"])
        assert result.exit_code == 0
        # Should show block info
        assert "config" in result.output or "Block" in result.output
