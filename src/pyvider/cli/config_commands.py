#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import os
import tomllib
from typing import Any

import click
from provide.foundation.cli.decorators import flexible_options
from provide.foundation.console import pout

from pyvider.cli.context import PyviderContext, pass_ctx


@click.group()
@flexible_options  # Allow logging control at the config group level
@pass_ctx
def config(ctx: PyviderContext, **kwargs: Any) -> None:
    """Manage and display Pyvider configuration."""
    pass


@config.command(name="show")
@pass_ctx
def show_config(ctx: PyviderContext) -> None:
    """Displays the current Pyvider configuration from all sources."""
    pout("🛠️  Pyvider Configuration:", style="bold")

    # --- File Configuration Section ---
    pout("\n📋 TOML Configuration File:", style="cyan")
    config_override = os.environ.get("PYVIDER_CONFIG_FILE")
    if config_override:
        pout("  Source: PYVIDER_CONFIG_FILE environment variable", style="magenta")
        pout(f"  Path:   {config_override}")
    else:
        pout("  Source: Default search path")
        pout("  Path:   ./pyvider.toml")

    loaded_path = ctx.config.loaded_file_path
    if loaded_path:
        try:
            with loaded_path.open("rb") as f:
                data = tomllib.load(f)
                for key, value in data.items():
                    display_val = f"'{value}'" if isinstance(value, str) else value
                    if "secret" in key or "token" in key:
                        display_val = "'********' (sensitive)"
                    pout(f"    - {key} = {display_val}")
        except Exception as e:
            pout(f"    ❌ Error reading file: {e}", style="red")
    else:
        pout("  Status: ⚠️  Not Found", style="yellow")

    # --- Environment Variable Section ---
    found_env_var = False
    for key, value in sorted(os.environ.items()):
        if key.startswith("PYVIDER_"):
            found_env_var = True
            display_value = value
            if "SECRET" in key or "TOKEN" in key:
                display_value = f"******** (Set, length: {len(value)})"
            pout(f"  {key}: {display_value}")
    if not found_env_var:
        pout("  (No PYVIDER_* environment variables set)")

    # --- Derived Settings Section ---
    pout(f"  Detected Terraform OS: {ctx.tf_os}")
    pout(f"  Detected Terraform Architecture: {ctx.tf_arch}")
    pout(f"  Effective Provider Version: {ctx.pyvider_version}")
    pout(f"  Terraform Plugin Directory: {ctx.tf_plugin_dir}")


# 🐍🏗️🔚
