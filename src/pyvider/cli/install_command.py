#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from pathlib import Path
import shutil
import sys

import click
from provide.foundation.console import perr, pout
from provide.foundation.file import safe_read_text

from pyvider.cli.context import PyviderContext
from pyvider.cli.utils import _find_actual_venv, _place_terraform_provider_script


def is_running_as_binary() -> bool:
    """
    Checks if the script is running as a compiled binary (e.g., via PyInstaller or PSPF).
    """
    return getattr(sys, "frozen", False)


def _remove_provider_script(ctx: PyviderContext, quiet: bool) -> None:
    target_provider_path = ctx.tf_plugin_dir / f"terraform-provider-{ctx.provider_name}"
    if target_provider_path.exists():
        target_provider_path.unlink()
        if not quiet:
            pout(f"  Provider script removed: {target_provider_path}", style="cyan")
    else:
        if not quiet:
            pout(f"  Provider script not found at: {target_provider_path}", style="yellow")


def _remove_empty_parent_dirs(ctx: PyviderContext, quiet: bool) -> None:
    try:
        parent = ctx.tf_plugin_dir.parent
        if parent.exists() and not any(parent.iterdir()):
            parent.rmdir()
            if not quiet:
                pout(f"  Cleaned up empty directory: {parent}", style="cyan")
    except OSError:
        # Silently ignore if we can't remove directory (e.g., it's not empty)
        pass


def _remove_venv_symlink(ctx: PyviderContext, quiet: bool) -> None:
    """Remove the provider symlink from venv bin directory if it exists."""
    venv_dir = _find_actual_venv(Path.cwd())
    if venv_dir:
        venv_bin = venv_dir / "bin"
        symlink_path = venv_bin / f"terraform-provider-{ctx.provider_name}"
        if symlink_path.exists() or symlink_path.is_symlink():
            symlink_path.unlink()
            if not quiet:
                pout(f"  Removed venv symlink: {symlink_path}", style="cyan")


def _uninstall_provider(ctx: PyviderContext, quiet: bool = False) -> None:
    """
    Uninstall the Terraform provider.

    Removes the provider script from the plugin directory and the symlink from venv.

    Args:
        ctx: The Pyvider context
        quiet: If True, suppress output for non-error messages
    """
    try:
        _remove_provider_script(ctx, quiet)
        _remove_venv_symlink(ctx, quiet)
        _remove_empty_parent_dirs(ctx, quiet)

        if not quiet:
            pout("✅ Provider uninstalled successfully", fg="green", bold=True)

    except Exception as e:
        pout(f"❌ Failed to uninstall provider: {e}", fg="red", bold=True)
        raise click.Abort() from e


def _is_pyvider_project() -> bool:
    pyproject_path = Path.cwd() / "pyproject.toml"
    pyvider_toml_path = Path.cwd() / "pyvider.toml"
    soup_toml_path = Path.cwd() / "soup.toml"
    if pyvider_toml_path.exists() or soup_toml_path.exists():
        return True
    elif pyproject_path.exists():
        try:
            content = safe_read_text(pyproject_path)
            if "[tool.pyvider]" in content or "[pyvider]" in content:
                return True
        except Exception:
            pass  # File doesn't exist or can't be read
    return False


def _install_binary_provider(pyvider_ctx: PyviderContext) -> None:
    try:
        source_binary_path = Path(sys.executable).resolve()
        target_dir = pyvider_ctx.tf_plugin_dir
        target_binary_path = target_dir / source_binary_path.name

        pout(f"  Source: {source_binary_path}")
        pout(f"  Target Directory: {target_dir}")

        if not target_dir.exists():
            pout(f"  Creating plugin directory: {target_dir}")
            target_dir.mkdir(parents=True, exist_ok=True)

        if target_binary_path.exists():
            pout(
                f"  ⚠️  Warning: Existing provider binary found at {target_binary_path}. It will be replaced.",
                fg="yellow",
            )

        pout(f"  Copying binary to {target_binary_path}...")
        shutil.copy2(source_binary_path, target_binary_path)

        pout("  Ensuring target binary is executable...")
        target_binary_path.chmod(target_binary_path.stat().st_mode | 0o111)

        pout("\n✅ Success! Provider binary installed.", fg="green", bold=True)

    except Exception as e:
        pout(f"\n❌ Failed to install provider binary: {e}", fg="red", bold=True)
        raise click.Abort() from e


def _install_dev_provider(pyvider_ctx: PyviderContext) -> None:
    pout("📝 Running in Development Mode.", fg="yellow")
    pout("  Placing development wrapper script for Terraform...")
    try:
        # Directly call the utility to place the provider script.
        _place_terraform_provider_script(pyvider_ctx)
    except Exception as e:
        pout(
            f"\n❌ Failed to place development wrapper script: {e}",
            fg="red",
            bold=True,
        )
        raise click.Abort() from e


@click.command(name="install")
@click.option(
    "--uninstall",
    is_flag=True,
    help="Uninstall the provider instead of installing it.",
)
@click.option(
    "--reinstall",
    is_flag=True,
    help="Uninstall and then install the provider.",
)
@click.pass_context
def install_command(
    ctx: click.Context,
    uninstall: bool,
    reinstall: bool,
) -> None:
    """
    Installs the provider for use with Terraform.

    In binary mode, it copies the executable. In development mode, it places
    the wrapper script.

    Use --uninstall to remove the provider, or --reinstall to refresh the installation.
    """
    pyvider_ctx: PyviderContext = ctx.obj

    # Validate mutually exclusive flags
    if uninstall and reinstall:
        perr(
            "Error: --uninstall and --reinstall are mutually exclusive.",
            fg="red",
            bold=True,
        )
        raise click.Abort()

    # Guard: Check for pyvider.toml or pyproject.toml with [tool.pyvider]
    if not _is_pyvider_project():
        perr(
            "Error: This command must be run from a directory containing a pyvider.toml file or a pyproject.toml file with a [tool.pyvider] section.",
            fg="red",
            bold=True,
        )
        raise click.Abort()

    # Handle uninstall (after validation)
    if uninstall:
        pout("🗑️  Uninstalling provider...", fg="yellow")
        _uninstall_provider(pyvider_ctx)
        return

    # Handle reinstall (uninstall + install)
    if reinstall:
        pout("🔄 Reinstalling provider...", fg="yellow")
        _uninstall_provider(pyvider_ctx, quiet=True)
        # Fall through to install logic below

    if is_running_as_binary():
        _install_binary_provider(pyvider_ctx)
    else:
        _install_dev_provider(pyvider_ctx)


# 🐍🏗️🔚
