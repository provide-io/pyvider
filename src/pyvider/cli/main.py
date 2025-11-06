#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

import click
from provide.foundation.cli.decorators import flexible_options, output_options
from provide.foundation.config import get_env
from provide.foundation.console import perr, pout

from pyvider.cli.context import PyviderContext


def _show_interactive_mode(ctx: click.Context) -> None:
    """Show interactive mode welcome message with launch context."""
    from pyvider.common.launch_context import detect_launch_context

    launch_context = detect_launch_context()

    pout("\n╭─────────────────────────────────────────────────╮", fg="cyan")
    pout("│           Interactive Mode                      │", fg="cyan", bold=True)
    pout("╰─────────────────────────────────────────────────╯", fg="cyan")

    pout("\nPyvider is running in interactive mode.")
    pout("To start the provider server for testing, use:\n")

    # Get the command name from the context
    cmd_name = ctx.command_path or "pyvider"
    pout(f"  {cmd_name} provide --force", fg="green", bold=True)

    pout("\n" + "─" * 50)
    pout("\nLaunch Context:", fg="cyan", bold=True)
    pout(f"  Method: {launch_context.method.value}", fg="white")
    pout(f"  Executable: {launch_context.executable_path}", fg="white")
    pout(f"  Python: {launch_context.python_executable}", fg="white")
    pout(f"  Working Directory: {launch_context.working_directory}", fg="white")

    pout("\n" + "─" * 50)
    pout("\nFor more information, use:")
    pout(f"  {cmd_name} --help", fg="yellow")
    pout(f"  {cmd_name} launch-context", fg="yellow")
    pout("")


@click.group(invoke_without_command=True)
@flexible_options  # Add logging and config options at root level
@output_options  # Add output format options
@click.pass_context
def cli(ctx: click.Context, **kwargs: Any) -> None:
    """
    Pyvider CLI Tool.

    When run by Terraform (detected via PLUGIN_MAGIC_COOKIE environment variable),
    this will automatically default to the 'provide' command.
    """
    # Ensure the custom context object is created and attached
    # at the top level of the application. This makes it available to all
    # subcommands via `ctx.obj`.
    if ctx.obj is None:
        ctx.obj = PyviderContext()

    # Store the CLI options in the context for subcommands to access
    for key, value in kwargs.items():
        if value is not None:
            setattr(ctx.obj, key, value)

    if ctx.invoked_subcommand is None:
        # Check if we're being run by Terraform via the magic cookie
        if get_env("TF_PLUGIN_MAGIC_COOKIE"):
            # Terraform is launching us - go into provider mode
            provide_command = cli.get_command(ctx, "provide")
            if provide_command:
                ctx.invoke(provide_command)
            else:
                # This case should not happen if the CLI is assembled correctly.
                perr("Error: Default command 'provide' not found.")
                pout(cli.get_help(ctx))
        else:
            # Not being run by Terraform - show interactive mode
            _show_interactive_mode(ctx)


# This decorator is for our custom context object, which is correct for subcommands.
pass_ctx = click.make_pass_decorator(PyviderContext, ensure=True)

# 🐍🏗️🔚
