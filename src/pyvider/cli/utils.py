"""Internal utilities for the Pyvider CLI tool."""

import datetime
from pathlib import Path

from provide.foundation.console import pout
from provide.foundation.file import atomic_write_text, ensure_dir
from provide.foundation.process import run
from provide.foundation.utils import timed_block

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


def _run_command(
    command: list[str] | str,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    check: bool = True,
    title: str = "",
) -> str:
    cmd_str = " ".join(command)
    effective_cwd = cwd or Path.cwd()

    log_dir = Path.home() / ".pyvider" / "logs"
    ensure_dir(log_dir)  # Foundation's safe directory creation
    log_file_path = log_dir / "prep.log"

    timestamp = datetime.datetime.now().isoformat()
    log_entry_header = f"--- Log Entry: {timestamp} ---\n"
    log_entry_cmd = f"Command: {cmd_str}\n"
    log_entry_cwd = f"CWD: {effective_cwd}\n"

    step_title = title or cmd_str
    pout(f"⏳ {step_title}...", style="cyan", end="")

    try:
        with timed_block() as timer:
            # Use foundation's process runner with better error handling
            result = run(
                command,
                cwd=effective_cwd,
                env=env,
                check=False,  # We handle return codes ourselves
            )
        stdout_str, stderr_str = result.stdout, result.stderr
        return_code = result.returncode

        # Use foundation's safe file operations for atomic logging
        log_content = (
            f"{log_entry_header}"
            f"{log_entry_cmd}"
            f"{log_entry_cwd}"
            f"Duration: {timer.elapsed:.2f}s\n"
            f"STDOUT:\n{stdout_str}\n"
            f"STDERR:\n{stderr_str}\n"
            f"Return Code: {return_code}\n---\n\n"
        )

        # Append to existing log file safely
        existing_content = ""
        if log_file_path.exists():
            existing_content = log_file_path.read_text(encoding="utf-8")

        atomic_write_text(log_file_path, existing_content + log_content)

        if check and return_code != 0:
            pout(" ❌ FAILED", style="red")
            error_message = f"Command failed with exit code {return_code}. Details in {log_file_path}"
            pout(error_message, style="red")
            from provide.foundation.process import ProcessError

            raise ProcessError(
                f"Command failed with exit code {return_code}",
                exit_code=return_code,
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
            )
        else:
            pout(f" ✅ Done ({timer.elapsed:.2f}s)", style="green")
        return stdout_str

    except Exception as e:
        pout(" ❌ ERROR", style="red")
        error_message = f"Failed to run command '{cmd_str}': {e}. Details may be in {log_file_path}"
        pout(error_message, style="red")
        raise


def _place_terraform_provider_script(ctx: PyviderContext) -> None:
    """
    Generates and places a Terraform provider wrapper script with accurate paths.

    Detects the actual virtual environment location and pyvider installation method,
    then generates a script with hardcoded accurate paths (no runtime detection).
    """
    try:
        if not ctx.tf_plugin_dir.exists():
            ctx.tf_plugin_dir.mkdir(parents=True, exist_ok=True)

        target_provider_path = ctx.tf_plugin_dir / "terraform-provider-pyvider"
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
            exec_line = 'exec pyvider provide "$@"'
            install_method = "installed (pyvider command)"
        else:
            # Use python -m for editable installs or when pyvider command doesn't exist
            exec_line = 'exec python -m pyvider.cli provide "$@"'
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
