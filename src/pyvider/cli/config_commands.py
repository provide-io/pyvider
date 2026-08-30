#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import os
from pathlib import Path
import tomllib
from typing import Any

import click
from provide.foundation.cli.decorators import flexible_options
from provide.foundation.console import pout

from pyvider.cli.context import PyviderContext, pass_ctx


@click.group()
@flexible_options  # Allow logging control at the config group level
@pass_ctx
def config(ctx: PyviderContext, /, **kwargs: Any) -> None:
    """Manage and display Pyvider configuration."""


def _show_config_file_source() -> None:
    """Report where the TOML file is being looked for."""
    pout("\n📋 TOML Configuration File:", style="cyan")
    config_override = os.environ.get("PYVIDER_CONFIG_FILE")
    if config_override:
        pout("  Source: PYVIDER_CONFIG_FILE environment variable", style="magenta")
        pout(f"  Path:   {config_override}")
    else:
        pout("  Source: Default search path")
        pout("  Path:   ./pyvider.toml")


def _show_config_file_contents(loaded_path: Path | None) -> None:
    """Print the loaded TOML, with anything that looks like a secret masked."""
    if loaded_path is None:
        pout("  Status: ⚠️  Not Found", style="yellow")
        return
    try:
        with loaded_path.open("rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        pout(f"    ❌ Error reading file: {e}", style="red")
        return
    for key, value in data.items():
        display_val = f"'{value}'" if isinstance(value, str) else value
        if "secret" in key or "token" in key:
            display_val = "'********' (sensitive)"
        pout(f"    - {key} = {display_val}")


def _show_environment() -> None:
    """Print every PYVIDER_* variable, with secret values reduced to a length."""
    found_env_var = False
    for key, value in sorted(os.environ.items()):
        if not key.startswith("PYVIDER_"):
            continue
        found_env_var = True
        display_value = value
        if "SECRET" in key or "TOKEN" in key:
            display_value = f"******** (Set, length: {len(value)})"
        pout(f"  {key}: {display_value}")
    if not found_env_var:
        pout("  (No PYVIDER_* environment variables set)")


@config.command(name="show")
@pass_ctx
def show_config(ctx: PyviderContext) -> None:
    """Displays the current Pyvider configuration from all sources."""
    pout("🛠️  Pyvider Configuration:", style="bold")

    _show_config_file_source()
    _show_config_file_contents(ctx.config.loaded_file_path)
    _show_environment()

    pout(f"  Detected Terraform OS: {ctx.tf_os}")
    pout(f"  Detected Terraform Architecture: {ctx.tf_arch}")
    pout(f"  Effective Provider Version: {ctx.pyvider_version}")
    pout(f"  Terraform Plugin Directory: {ctx.tf_plugin_dir}")


# 🐍🏗️🔚
