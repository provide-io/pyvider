from pathlib import Path
import shutil
import sys

import click
from provide.foundation.console import perr
from provide.foundation.file import safe_read_text

from pyvider.cli.context import PyviderContext

# Import the correct command for placing the provider script.
from pyvider.cli.prep_commands import prep_provider
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


def x_is_running_as_binary__mutmut_orig() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, "frozen", False)


def x_is_running_as_binary__mutmut_1() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(None, "frozen", False)


def x_is_running_as_binary__mutmut_2() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, None, False)


def x_is_running_as_binary__mutmut_3() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, "frozen", None)


def x_is_running_as_binary__mutmut_4() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr("frozen", False)


def x_is_running_as_binary__mutmut_5() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, False)


def x_is_running_as_binary__mutmut_6() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, "frozen", )


def x_is_running_as_binary__mutmut_7() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, "XXfrozenXX", False)


def x_is_running_as_binary__mutmut_8() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, "FROZEN", False)


def x_is_running_as_binary__mutmut_9() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, "frozen", True)

x_is_running_as_binary__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_running_as_binary__mutmut_1': x_is_running_as_binary__mutmut_1, 
    'x_is_running_as_binary__mutmut_2': x_is_running_as_binary__mutmut_2, 
    'x_is_running_as_binary__mutmut_3': x_is_running_as_binary__mutmut_3, 
    'x_is_running_as_binary__mutmut_4': x_is_running_as_binary__mutmut_4, 
    'x_is_running_as_binary__mutmut_5': x_is_running_as_binary__mutmut_5, 
    'x_is_running_as_binary__mutmut_6': x_is_running_as_binary__mutmut_6, 
    'x_is_running_as_binary__mutmut_7': x_is_running_as_binary__mutmut_7, 
    'x_is_running_as_binary__mutmut_8': x_is_running_as_binary__mutmut_8, 
    'x_is_running_as_binary__mutmut_9': x_is_running_as_binary__mutmut_9
}

def is_running_as_binary(*args, **kwargs):
    result = _mutmut_trampoline(x_is_running_as_binary__mutmut_orig, x_is_running_as_binary__mutmut_mutants, args, kwargs)
    return result 

is_running_as_binary.__signature__ = _mutmut_signature(x_is_running_as_binary__mutmut_orig)
x_is_running_as_binary__mutmut_orig.__name__ = 'x_is_running_as_binary'


@click.command(name="install")
@click.pass_context
def install_command(ctx: click.Context) -> None:  # noqa: C901
    """
    Installs the provider for use with Terraform.

    In binary mode, it copies the executable. In development mode, it places
    the wrapper script.
    """
    pyvider_ctx: PyviderContext = ctx.obj

    # Guard: Check for pyvider.toml or pyproject.toml with [tool.pyvider]
    pyproject_path = Path.cwd() / "pyproject.toml"
    pyvider_toml_path = Path.cwd() / "pyvider.toml"
    is_pyvider_project = False
    if pyvider_toml_path.exists():
        is_pyvider_project = True
    elif pyproject_path.exists():
        try:
            content = safe_read_text(pyproject_path)
            if "[tool.pyvider]" in content:
                is_pyvider_project = True
        except Exception:
            pass  # File doesn't exist or can't be read

    if not is_pyvider_project:
        perr(
            "Error: This command must be run from a directory containing a pyvider.toml file or a pyproject.toml file with a [tool.pyvider] section.",
            fg="red",
            bold=True,
        )
        raise click.Abort()

    if is_running_as_binary():
        click.secho("📦 Running in Binary Mode.", fg="cyan")
        try:
            source_binary_path = Path(sys.executable).resolve()
            target_dir = pyvider_ctx.tf_plugin_dir
            target_binary_path = target_dir / source_binary_path.name

            click.echo(f"  Source: {source_binary_path}")
            click.echo(f"  Target Directory: {target_dir}")

            if not target_dir.exists():
                click.echo(f"  Creating plugin directory: {target_dir}")
                target_dir.mkdir(parents=True, exist_ok=True)

            if target_binary_path.exists():
                click.secho(
                    f"  ⚠️  Warning: Existing provider binary found at {target_binary_path}. It will be replaced.",
                    fg="yellow",
                )

            click.echo(f"  Copying binary to {target_binary_path}...")
            shutil.copy2(source_binary_path, target_binary_path)

            click.echo("  Ensuring target binary is executable...")
            target_binary_path.chmod(target_binary_path.stat().st_mode | 0o111)

            click.secho(
                f"\n✅ Success! Provider '{source_binary_path.name}' installed for Terraform.",
                fg="green",
                bold=True,
            )

        except Exception as e:
            click.secho(f"\n❌ Failed to install provider binary: {e}", fg="red", bold=True)
            raise click.Abort() from e
    else:
        click.secho("📝 Running in Development Mode.", fg="yellow")
        click.echo("  Placing development wrapper script for Terraform...")
        try:
            # Invoke the command that places the provider script, not the one
            # that installs Terraform itself.
            ctx.invoke(prep_provider)
        except Exception as e:
            click.secho(
                f"\n❌ Failed to place development wrapper script: {e}",
                fg="red",
                bold=True,
            )
            raise click.Abort() from e
