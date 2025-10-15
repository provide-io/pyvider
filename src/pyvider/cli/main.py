from typing import Any

import click
from provide.foundation.cli.decorators import flexible_options, output_options
from provide.foundation.console import perr

from pyvider.cli.context import PyviderContext


@click.group(invoke_without_command=True)
@flexible_options  # Add logging and config options at root level
@output_options  # Add output format options
@click.pass_context
def cli(ctx: click.Context, **kwargs: Any) -> None:
    """
    Pyvider CLI Tool.

    When run by Terraform (with no subcommands), this will automatically
    default to the 'provide' command.
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
        # This is the default action when no subcommand is given.
        # We find the 'provide' command and invoke it.
        provide_command = cli.get_command(ctx, "provide")
        if provide_command:
            ctx.invoke(provide_command)
        else:
            # This case should not happen if the CLI is assembled correctly.
            perr("Error: Default command 'provide' not found.")
            click.echo(cli.get_help(ctx))


# This decorator is for our custom context object, which is correct for subcommands.
pass_ctx = click.make_pass_decorator(PyviderContext, ensure=True)
