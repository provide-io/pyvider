from pathlib import Path
import shutil
import sys

import click
from provide.foundation.console import perr
from provide.foundation.file import safe_read_text

from pyvider.cli.context import PyviderContext

# Import the correct command for placing the provider script.
from pyvider.cli.prep_commands import prep_provider


def is_running_as_binary() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, "frozen", False)


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
