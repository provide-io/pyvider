import asyncio
import sys

import click

from pyvider.hub.components import get_hub_diagnostics, registry
from pyvider.hub.discovery import ComponentDiscovery
from pyvider.schema import PvsAttribute, PvsNestedBlock, PvsObjectType, PvsSchema

from provide.foundation.cli.decorators import flexible_options
from pyvider.cli.main import PyviderContext, cli, pass_ctx


def _handle_discovery_errors(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        click.secho("\n" + "─" * 70, fg="red")
        click.secho(
            " ❌ Critical Error: Component Discovery Failed", fg="red", bold=True
        )
        click.secho("─" * 70, fg="red")
        click.echo(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        click.echo("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            click.secho(f"  - Module: {module_name}", fg="yellow")
            click.secho(f"    Error: {error}", fg="white")

        click.secho("\n" + "─" * 70, fg="red")
        click.secho("Action Required:", fg="yellow", bold=True)
        click.echo(
            "  1. Ensure all dependencies listed in 'pyproject.toml' are installed."
        )
        click.echo(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        click.echo(
            "  3. Verify that all local component packages are correctly structured."
        )
        sys.exit(1)


# --- Helper Functions for Displaying Schemas ---
def _display_attribute(attr: PvsAttribute, indent_level: int) -> None:
    indent = "  " * indent_level
    flags = []
    if attr.required:
        flags.append(click.style("Required", fg="bright_red"))
    if attr.optional:
        flags.append(click.style("Optional", fg="bright_blue"))
    if attr.computed:
        flags.append(click.style("Computed", fg="bright_cyan"))
    if attr.sensitive:
        flags.append(click.style("Sensitive", fg="magenta"))
    flag_str = f" ({', '.join(flags)})" if flags else ""
    click.echo(f"{indent}Attribute: {click.style(attr.name, fg='yellow')}{flag_str}")
    type_str = str(attr.type)
    click.echo(f"{indent}  - Type: {click.style(type_str, fg='green')}")
    if attr.description:
        click.echo(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        click.echo(f"{indent}  - Default: {attr.default}")


def _display_block_type(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    click.echo(
        f"{indent}Block: {click.style(block_def.type_name, fg='bright_yellow')} {nesting_str}"
    )
    if block_def.description:
        click.echo(f"{indent}  - Description: {block_def.description}")
    _display_block_content(block_def.block, indent_level + 1)


def _display_block_content(block: PvsObjectType, indent_level: int) -> None:
    if block.attributes:
        for attr in block.attributes.values():
            _display_attribute(attr, indent_level + 1)
    if block.block_types:
        for nested_block in block.block_types:
            _display_block_type(nested_block, indent_level + 1)


# --- Main 'components' Group ---
@cli.group()
@flexible_options  # Allow logging control at the component group level
@pass_ctx
def components(ctx: PyviderContext, **kwargs) -> None:
    """Manage, inspect, and diagnose Pyvider components."""
    # THE FIX: Run discovery and error handling for the entire command group.
    asyncio.run(
        ctx._ensure_components_discovered(
            registry, ComponentDiscovery, click.echo, click.secho
        )
    )
    _handle_discovery_errors(ctx)


# --- Core Component Commands ---
@components.command(name="list")
@pass_ctx
def list_components(ctx: PyviderContext) -> None:
    """Lists all available Pyvider components."""
    all_comps = registry.list_components()
    if not any(all_comps.values()):
        click.secho("No components found.", fg="yellow")
        return
    for comp_type, comps_dict in sorted(all_comps.items()):
        if comps_dict:
            click.secho(f"\n{comp_type.capitalize()}:", fg="bright_cyan", bold=True)
            for name in sorted(comps_dict.keys()):
                click.secho(f"  - {name}")


@components.command(name="show")
@click.argument("component_type")
@click.argument("component_name")
@pass_ctx
def show_component(
    ctx: PyviderContext, component_type: str, component_name: str
) -> None:
    """
    Shows detailed information and schema for a specific component.
    """
    comp_type_lower = component_type.lower()
    component = registry.get_component(comp_type_lower, component_name)
    if not component:
        click.secho(
            f"Component '{component_name}' of type '{comp_type_lower}' not found.",
            fg="red",
        )
        return
    click.secho(
        f"\nSchema for {comp_type_lower}: {click.style(component_name, bold=True, fg='bright_white')}"
    )
    click.echo("=" * (20 + len(comp_type_lower) + len(component_name)))
    if comp_type_lower == "singleton" and hasattr(component, "schema"):
        schema = component.schema
    elif hasattr(component, "get_schema"):
        schema = component.get_schema()
    else:
        click.secho("This component does not expose a schema.", fg="yellow")
        return
    if not isinstance(schema, PvsSchema):
        click.secho(
            "Component's schema method did not return a PvsSchema object.", fg="red"
        )
        return
    if schema.block.description:
        click.secho(f"\n{schema.block.description}\n", italic=True)
    _display_block_content(schema.block, 0)
    click.echo()


@components.command(name="diagnostics")
@pass_ctx
def show_diagnostics(ctx: PyviderContext) -> None:
    """Shows detailed autodiscovery diagnostics from the component hub."""
    click.secho("📊 Hub Diagnostics", bold=True)
    click.echo("=" * 30)
    try:
        diagnostics = get_hub_diagnostics()
        click.echo(f"🔢 Total component types: {diagnostics['total_component_types']}")
        click.echo(f"🔢 Total components: {diagnostics['total_components']}")
        click.echo("\n📋 Component breakdown:")
        for comp_type, count in diagnostics["component_breakdown"].items():
            click.echo(f"  - {comp_type}: {count}")
    except Exception as e:
        click.secho(f"❌ Failed to get diagnostics: {e}", fg="red")
