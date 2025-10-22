from typing import Any

import click
from provide.foundation.cli.decorators import flexible_options, output_options
from provide.foundation.console import perr

from pyvider.cli.context import PyviderContext
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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
