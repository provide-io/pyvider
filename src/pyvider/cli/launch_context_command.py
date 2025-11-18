#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""CLI command for inspecting Pyvider launch context."""

import json

import click
from provide.foundation.console import pout

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

        pout(json.dumps(data, indent=2))

    else:
        # Human-readable format
        pout("\n🚀 Pyvider Launch Context", fg="green", bold=True)
        pout("─" * 50, fg="green")

        pout("\nLaunch Method: ", fg="cyan", bold=True, nl=False)
        pout(launch_context.method.value, fg="white")

        pout("Executable Path: ", fg="cyan", bold=True, nl=False)
        pout(launch_context.executable_path, fg="white")

        pout("Python Executable: ", fg="cyan", bold=True, nl=False)
        pout(launch_context.python_executable, fg="white")

        pout("Working Directory: ", fg="cyan", bold=True, nl=False)
        pout(launch_context.working_directory, fg="white")

        pout("Terraform Invoked: ", fg="cyan", bold=True, nl=False)
        color = "green" if launch_context.is_terraform_invoked else "red"
        pout(str(launch_context.is_terraform_invoked), fg=color)

        # Show method-specific details
        if launch_context.details:
            pout("\nMethod Details:", fg="cyan", bold=True)
            for key, value in launch_context.details.items():
                pout(f"  {key}: ", fg="cyan", nl=False)

                # Format complex values
                if isinstance(value, (list, dict)):
                    if len(str(value)) > 80:
                        pout("<complex_value>", fg="yellow")
                    else:
                        pout(str(value), fg="white")
                else:
                    pout(str(value), fg="white")

        # Show environment info if verbose
        if verbose:
            pout("\nEnvironment Information:", fg="cyan", bold=True)
            env_info = launch_context.environment_info

            for key, value in env_info.items():
                if key == "argv":
                    pout(f"  {key}: ", fg="cyan", nl=False)
                    pout(" ".join(value), fg="white")
                elif key == "pspf_env_vars" and value:
                    pout("  PSPF Environment Variables:", fg="cyan")
                    for env_key, env_value in value.items():
                        pout(f"    {env_key}: {env_value}", fg="white")
                else:
                    pout(f"  {key}: ", fg="cyan", nl=False)
                    if isinstance(value, str) and len(value) > 100:
                        pout(f"{value[:100]}...", fg="white")
                    else:
                        pout(str(value), fg="white")

        pout("\n" + "─" * 50, fg="green")

        # Add helpful information based on launch method
        _show_method_specific_help(launch_context.method)


def _show_method_specific_help(method: LaunchMethod) -> None:
    """Show helpful information based on the detected launch method."""
    if method.value == "pspf_package":
        pout("\n💡 PSPF Package Detected", fg="blue", bold=True)
        pout("  This provider is running from a PSPF (Progressive Secure Package Format)")
        pout("  self-contained package with embedded Python runtime.")

    elif method.value == "script_module":
        pout("\n💡 Module Launch Detected", fg="blue", bold=True)
        pout("  This provider was launched using 'python -m pyvider' or similar.")
        pout("  This is typically used during development or testing.")

    elif method.value == "editable_install":
        pout("\n💡 Development Mode Detected", fg="blue", bold=True)
        pout("  This provider is running from an editable install (pip install -e).")
        pout("  This is typically used during development.")

    elif method.value == "script_direct":
        pout("\n💡 Direct Script Launch Detected", fg="blue", bold=True)
        pout("  This provider is running as a direct Python script.")

    elif method.value == "unknown":
        pout("\n⚠️ Unknown Launch Method", fg="yellow", bold=True)
        pout("  The launch method could not be determined.")
        pout("  Use --verbose flag for more debugging information.")


# 🐍🏗️🔚
