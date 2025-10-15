"""
CLI command for inspecting Pyvider launch context.
"""

import json

import click

from pyvider.cli.main import cli
from pyvider.common.launch_context import LaunchMethod


@cli.command("launch-context")
@click.option(
    "--format",
    type=click.Choice(["human", "json"], case_sensitive=False),
    default="human",
    help="Output format for launch context information.",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Show detailed information including environment variables.",
)
def launch_context_cmd(format: str, verbose: bool) -> None:  # noqa: C901
    """
    Display detailed information about how Pyvider was launched.

    This command analyzes the current execution environment and reports:
    - Launch method (PSPF package, script, module, etc.)
    - Executable paths and Python environment
    - Relevant environment variables
    - Additional context based on launch method
    """
    from pyvider.common.launch_context import detect_launch_context

    launch_context = detect_launch_context()

    if format.lower() == "json":
        # Convert to JSON-serializable format
        data = {
            "method": launch_context.method.value,
            "executable_path": launch_context.executable_path,
            "python_executable": launch_context.python_executable,
            "working_directory": launch_context.working_directory,
            "is_terraform_invoked": launch_context.is_terraform_invoked,
            "details": launch_context.details,
        }

        if verbose:
            data["environment_info"] = launch_context.environment_info

        click.echo(json.dumps(data, indent=2))

    else:
        # Human-readable format
        click.secho("\n🚀 Pyvider Launch Context", fg="green", bold=True)
        click.secho("─" * 50, fg="green")

        click.secho("\nLaunch Method: ", fg="cyan", bold=True, nl=False)
        click.secho(launch_context.method.value, fg="white")

        click.secho("Executable Path: ", fg="cyan", bold=True, nl=False)
        click.secho(launch_context.executable_path, fg="white")

        click.secho("Python Executable: ", fg="cyan", bold=True, nl=False)
        click.secho(launch_context.python_executable, fg="white")

        click.secho("Working Directory: ", fg="cyan", bold=True, nl=False)
        click.secho(launch_context.working_directory, fg="white")

        click.secho("Terraform Invoked: ", fg="cyan", bold=True, nl=False)
        color = "green" if launch_context.is_terraform_invoked else "red"
        click.secho(str(launch_context.is_terraform_invoked), fg=color)

        # Show method-specific details
        if launch_context.details:
            click.secho("\nMethod Details:", fg="cyan", bold=True)
            for key, value in launch_context.details.items():
                click.secho(f"  {key}: ", fg="cyan", nl=False)

                # Format complex values
                if isinstance(value, (list, dict)):
                    if len(str(value)) > 80:
                        click.secho("<complex_value>", fg="yellow")
                    else:
                        click.secho(str(value), fg="white")
                else:
                    click.secho(str(value), fg="white")

        # Show environment info if verbose
        if verbose:
            click.secho("\nEnvironment Information:", fg="cyan", bold=True)
            env_info = launch_context.environment_info

            for key, value in env_info.items():
                if key == "argv":
                    click.secho(f"  {key}: ", fg="cyan", nl=False)
                    click.secho(" ".join(value), fg="white")
                elif key == "pspf_env_vars" and value:
                    click.secho("  PSPF Environment Variables:", fg="cyan")
                    for env_key, env_value in value.items():
                        click.secho(f"    {env_key}: {env_value}", fg="white")
                else:
                    click.secho(f"  {key}: ", fg="cyan", nl=False)
                    if isinstance(value, str) and len(value) > 100:
                        click.secho(f"{value[:100]}...", fg="white")
                    else:
                        click.secho(str(value), fg="white")

        click.secho("\n" + "─" * 50, fg="green")

        # Add helpful information based on launch method
        _show_method_specific_help(launch_context.method)


def _show_method_specific_help(method: LaunchMethod) -> None:
    """Show helpful information based on the detected launch method."""
    if method.value == "pspf_package":
        click.secho("\n💡 PSPF Package Detected", fg="blue", bold=True)
        click.echo("  This provider is running from a PSPF (Progressive Secure Package Format)")
        click.echo("  self-contained package with embedded Python runtime.")

    elif method.value == "script_module":
        click.secho("\n💡 Module Launch Detected", fg="blue", bold=True)
        click.echo("  This provider was launched using 'python -m pyvider' or similar.")
        click.echo("  This is typically used during development or testing.")

    elif method.value == "editable_install":
        click.secho("\n💡 Development Mode Detected", fg="blue", bold=True)
        click.echo("  This provider is running from an editable install (pip install -e).")
        click.echo("  This is typically used during development.")

    elif method.value == "script_direct":
        click.secho("\n💡 Direct Script Launch Detected", fg="blue", bold=True)
        click.echo("  This provider is running as a direct Python script.")

    elif method.value == "unknown":
        click.secho("\n⚠️ Unknown Launch Method", fg="yellow", bold=True)
        click.echo("  The launch method could not be determined.")
        click.echo("  Use --verbose flag for more debugging information.")
