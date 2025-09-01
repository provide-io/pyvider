import click
from provide.foundation.cli.decorators import standard_options

from pyvider.cli.context import PyviderContext


@click.group(invoke_without_command=True)
@standard_options  # Add foundation's standard CLI options (--debug, --verbose, --quiet)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Pyvider CLI Tool.

    When run by Terraform (with no subcommands), this will automatically
    default to the 'provide' command.
    """
    # THE FIX: Ensure the custom context object is created and attached
    # at the top level of the application. This makes it available to all
    # subcommands via `ctx.obj`.
    if ctx.obj is None:
        ctx.obj = PyviderContext()

    if ctx.invoked_subcommand is None:
        # This is the default action when no subcommand is given.
        # We find the 'provide' command and invoke it.
        provide_command = cli.get_command(ctx, "provide")
        if provide_command:
            ctx.invoke(provide_command)
        else:
            # This case should not happen if the CLI is assembled correctly.
            click.secho("Error: Default command 'provide' not found.", fg="red")
            click.echo(cli.get_help(ctx))


# This decorator is for our custom context object, which is correct for subcommands.
pass_ctx = click.make_pass_decorator(PyviderContext, ensure=True)
