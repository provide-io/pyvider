import os
import tomllib

import click

from pyvider.cli.context import PyviderContext, pass_ctx


@click.group()
@pass_ctx
def config(ctx: PyviderContext) -> None:
    """Manage and display Pyvider configuration."""
    pass


@config.command(name="show")
@pass_ctx
def show_config(ctx: PyviderContext) -> None:
    """Displays the current Pyvider configuration from all sources."""
    click.secho("Pyvider Configuration:", bold=True)

    # --- File Configuration Section ---
    click.secho("\nTOML Configuration File:", fg="cyan")
    config_override = os.environ.get("PYVIDER_CONFIG_FILE")
    if config_override:
        click.secho("  Source: PYVIDER_CONFIG_FILE environment variable", fg="magenta")
        click.echo(f"  Path:   {config_override}")
    else:
        click.echo("  Source: Default search path")
        click.echo("  Path:   ./pyvider.toml")

    loaded_path = ctx.config.loaded_file_path
    if loaded_path:
        click.secho("  Status: Found and Loaded", fg="green")
        try:
            with loaded_path.open("rb") as f:
                data = tomllib.load(f)
                for key, value in data.items():
                    display_val = f"'{value}'" if isinstance(value, str) else value
                    if "secret" in key or "token" in key:
                        display_val = "'********' (sensitive)"
                    click.echo(f"    - {key} = {display_val}")
        except Exception as e:
            click.secho(f"    Error reading file: {e}", fg="red")
    else:
        click.secho("  Status: Not Found", fg="yellow")

    # --- Environment Variable Section ---
    click.secho("\nEnvironment Variables (PYVIDER_*):", fg="cyan")
    found_env_var = False
    for key, value in sorted(os.environ.items()):
        if key.startswith("PYVIDER_"):
            found_env_var = True
            display_value = value
            if "SECRET" in key or "TOKEN" in key:
                display_value = f"******** (Set, length: {len(value)})"
            click.echo(f"  {key}: {display_value}")
    if not found_env_var:
        click.echo("  (No PYVIDER_* environment variables set)")

    # --- Derived Settings Section ---
    click.secho("\nDerived Settings:", fg="cyan")
    click.echo(f"  Detected Terraform OS: {ctx.tf_os}")
    click.echo(f"  Detected Terraform Architecture: {ctx.tf_arch}")
    click.echo(f"  Effective Provider Version: {ctx.pyvider_version}")
    click.echo(f"  Terraform Plugin Directory: {ctx.tf_plugin_dir}")
