#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Internal utilities for the Pyvider CLI tool."""

from pathlib import Path

from provide.foundation.console import pout
from provide.foundation.file import atomic_write_text

from pyvider.cli.context import PyviderContext


def _find_actual_venv(base_dir: Path) -> Path | None:
    """
    Find the actual virtual environment directory that exists.

    Searches for common venv locations in order of preference:
    1. .venv (standard)
    2. venv (alternative)
    3. .venv_* (platform-specific)
    4. workenv/*/ (wrkenv style)

    Args:
        base_dir: Directory to search in

    Returns:
        Path to venv directory if found, None otherwise
    """
    candidates = [
        base_dir / ".venv",
        base_dir / "venv",
    ]

    # Add platform-specific venvs
    candidates.extend(sorted(base_dir.glob(".venv_*")))

    # Add workenv style venvs
    candidates.extend(sorted(base_dir.glob("workenv/*/")))

    for venv_dir in candidates:
        activate_script = venv_dir / "bin" / "activate"
        if activate_script.exists():
            return venv_dir

    return None


def _create_venv_symlink(venv_dir: Path, provider_name: str) -> None:
    """
    Create a symlink for terraform-provider-{name} in the venv bin directory.

    This symlink allows the provider to be invoked with the correct binary name
    for Terraform's binary name detection, which is required for proper
    TF_PLUGIN_MAGIC_COOKIE recognition.

    Args:
        venv_dir: Path to the virtual environment directory
        provider_name: Name of the provider (e.g., "pyvider", "tofusoup")

    Raises:
        ConfigurationError: If symlink creation fails
    """
    try:
        venv_bin = venv_dir / "bin"
        symlink_path = venv_bin / f"terraform-provider-{provider_name}"
        target = Path("pyvider")  # Relative symlink to pyvider in same directory

        # Remove existing symlink if it exists
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()

        # Create the symlink
        symlink_path.symlink_to(target)
        pout(f"  Symlink created: {symlink_path} -> {target}", style="cyan")
    except Exception as e:
        from provide.foundation.errors import ConfigurationError

        raise ConfigurationError(f"Failed to create venv symlink: {e}") from e


def _remove_venv_symlink(venv_dir: Path, provider_name: str) -> None:
    """
    Remove the terraform-provider-{name} symlink from the venv bin directory.

    Args:
        venv_dir: Path to the virtual environment directory
        provider_name: Name of the provider (e.g., "pyvider", "tofusoup")

    Returns:
        None (silently succeeds even if symlink doesn't exist)
    """
    try:
        symlink_path = venv_dir / "bin" / f"terraform-provider-{provider_name}"
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
            pout(f"  Symlink removed: {symlink_path}", style="cyan")
    except Exception as e:
        pout(f"  Warning: Failed to remove venv symlink: {e}", style="yellow")


def _place_terraform_provider_script(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / f"terraform-provider-{ctx.provider_name}"
        install_dir = Path.cwd()

        # Detect actual virtual environment
        venv_dir = _find_actual_venv(install_dir)
        if not venv_dir:
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"No virtual environment found in {install_dir}. "
                f"Please run 'uv venv' or 'python -m venv .venv' first, "
                f"then run 'pyvider install' again."
            )

        # Validate Python executable exists
        python_exe = venv_dir / "bin" / "python"
        if not python_exe.exists():
            from provide.foundation.errors import ConfigurationError

            raise ConfigurationError(
                f"Python executable not found at {python_exe}. "
                f"Virtual environment at {venv_dir} may be corrupted."
            )

        # Check if pyvider command will be available (for installed mode)
        pyvider_cmd = venv_dir / "bin" / "pyvider"
        has_pyvider_cmd = pyvider_cmd.exists()

        # Determine execution method
        if has_pyvider_cmd:
            exec_line = 'exec pyvider "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli "$@"'
            install_method = "editable (python -m)"

        # Generate script with accurate, hardcoded paths
        script_content = f"""#!/bin/bash
# Pyvider Terraform Provider Wrapper Script (Development Mode)
# This script is auto-generated by 'pyvider install'
# Generated for: {install_method}
set -eo pipefail

# Installation directory (where 'pyvider install' was run)
INSTALL_DIR="{install_dir}"

# Virtual environment (detected at generation time)
VENV_PATH="{venv_dir}/bin/activate"

# Python executable
PYTHON_EXE="{python_exe}"

# Change to installation directory
cd "$INSTALL_DIR" || {{ echo "ERROR: Failed to cd to $INSTALL_DIR" >&2; exit 1; }}

# Activate virtual environment
if [ ! -f "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at '$VENV_PATH'" >&2
    echo "The venv may have been moved or deleted. Run 'pyvider install' again." >&2
    exit 1
fi
source "$VENV_PATH"

# Set Terraform plugin magic cookie
export PLUGIN_MAGIC_COOKIE_VALUE="$TF_PLUGIN_MAGIC_COOKIE"

# Execute provider
{exec_line}
"""

        atomic_write_text(target_provider_path, script_content)
        target_provider_path.chmod(target_provider_path.stat().st_mode | 0o111)

        # Report what was generated
        pout(f"  Virtual environment: {venv_dir.relative_to(install_dir)}", style="cyan")
        pout(f"  Execution method: {install_method}", style="cyan")
        pout(f"  Script location: {target_provider_path}", style="cyan")

    except Exception as e:
        pout(
            f"An unexpected error occurred placing provider script: {e}",
            style="red",
            bold=True,
        )
        raise


# 🐍🏗️🔚
