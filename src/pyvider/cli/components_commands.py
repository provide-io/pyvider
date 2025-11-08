#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import asyncio
import sys
import time
from typing import Any

import click
from provide.foundation.cli.decorators import flexible_options
from provide.foundation.console import perr, pout
from provide.foundation.formatting import format_table

from pyvider.cli.main import PyviderContext, cli, pass_ctx
from pyvider.hub.components import get_hub_diagnostics, registry
from pyvider.hub.discovery import ComponentDiscovery
from pyvider.schema import PvsAttribute, PvsNestedBlock, PvsObjectType, PvsSchema


def _handle_discovery_errors(ctx: PyviderContext) -> None:
    """Checks for and reports critical discovery errors, then exits."""
    if ctx.discovery_errors:
        perr("\n" + "─" * 70)
        perr(" ❌ Critical Error: Component Discovery Failed", style="bold")
        perr("─" * 70)
        perr(
            "\nOne or more component modules could not be imported. This usually indicates\n"
            "a missing dependency or a packaging problem."
        )
        perr("\nFailed Modules:")
        for module_name, error in ctx.discovery_errors:
            perr(f"  - Module: {module_name}", style="yellow")
            perr(f"    Error: {error}")

        perr("\n" + "─" * 70)
        perr("Action Required:", style="yellow bold")
        perr("  1. Ensure all dependencies listed in 'pyproject.toml' are installed.")
        perr(
            "  2. If developing locally, run 'uv pip install -e .[dev]' to install\n"
            "     the project in editable mode with all development dependencies."
        )
        perr("  3. Verify that all local component packages are correctly structured.")
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
    pout(f"{indent}Attribute: {attr.name}{flag_str}", style="yellow")
    type_str = str(attr.type)
    pout(f"{indent}  - Type: {type_str}", style="green")
    if attr.description:
        pout(f"{indent}  - Description: {attr.description}")
    if attr.default is not None:
        pout(f"{indent}  - Default: {attr.default}")


def _display_block_type(block_def: PvsNestedBlock, indent_level: int) -> None:
    indent = "  " * indent_level
    nesting_str = f"({block_def.nesting.name})"
    pout(f"{indent}Block: {block_def.type_name} {nesting_str}", style="bright_yellow")
    if block_def.description:
        pout(f"{indent}  - Description: {block_def.description}")
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
def components(ctx: PyviderContext, **kwargs: Any) -> None:
    """Manage, inspect, and diagnose Pyvider components."""
    # THE FIX: Run discovery and error handling for the entire command group.
    asyncio.run(ctx._ensure_components_discovered(registry, ComponentDiscovery, pout, pout))
    _handle_discovery_errors(ctx)


# --- Core Component Commands ---
@components.command(name="list")
@pass_ctx
def list_components(ctx: PyviderContext) -> None:
    """Lists all available Pyvider components."""
    all_comps = registry.list_components()
    if not any(all_comps.values()):
        pout("No components found.", fg="yellow")
        return
    for comp_type, comps_dict in sorted(all_comps.items()):
        if comps_dict:
            pout(f"\n{comp_type.capitalize()}:", fg="bright_cyan", bold=True)
            for name in sorted(comps_dict.keys()):
                pout(f"  - {name}")


@components.command(name="show")
@click.argument("component_type")
@click.argument("component_name")
@pass_ctx
def show_component(ctx: PyviderContext, component_type: str, component_name: str) -> None:
    """
    Shows detailed information and schema for a specific component.
    """
    comp_type_lower = component_type.lower()
    component = registry.get_component(comp_type_lower, component_name)
    if not component:
        perr(f"Component '{component_name}' of type '{comp_type_lower}' not found.")
        return
    pout(f"\n📋 Schema for {comp_type_lower}: {component_name}", style="bold bright_white")
    pout("=" * (20 + len(comp_type_lower) + len(component_name)))
    if comp_type_lower == "singleton" and hasattr(component, "schema"):
        schema = component.schema
    elif hasattr(component, "get_schema"):
        schema = component.get_schema()
    else:
        pout("This component does not expose a schema.", style="yellow")
        return
    if not isinstance(schema, PvsSchema):
        perr("Component's schema method did not return a PvsSchema object.")
        return
    if schema.block.description:
        pout(f"\n{schema.block.description}\n", style="italic")
    _display_block_content(schema.block, 0)
    pout("")


@components.command(name="diagnostics")
@pass_ctx
def show_diagnostics(ctx: PyviderContext) -> None:
    """Shows detailed autodiscovery diagnostics from the component hub."""
    pout("📊 Hub Diagnostics", style="bold")
    pout("=" * 30)

    try:
        start_time = time.perf_counter()
        diagnostics = get_hub_diagnostics()
        elapsed = time.perf_counter() - start_time

        # Summary stats
        pout(f"🔢 Total component types: {diagnostics['total_component_types']}")
        pout(f"🔢 Total components: {diagnostics['total_components']}")
        pout(f"⏱️  Discovery time: {elapsed:.3f}s")

        # Component breakdown table
        pout("\n📋 Component Breakdown:")

        # Prepare table data
        table_data = []
        for comp_type, count in diagnostics["component_breakdown"].items():
            table_data.append([comp_type.title(), str(count)])

        if table_data:
            # Use foundation's table formatter
            table = format_table(table_data, headers=["Component Type", "Count"], title="Components by Type")
            pout(table)
        else:
            pout("  No components discovered")

    except Exception as e:
        perr(f"❌ Failed to get diagnostics: {e}")


# 🐍🏗️🔚
