from pathlib import Path
import subprocess
import sys

import click
from provide.foundation.console import perr, pout

from pyvider.cli.context import PyviderContext, pass_ctx
from pyvider.cli.utils import _place_terraform_provider_script, _run_command


@click.group()
def prep() -> None:
    """Prepare Pyvider for use (e.g., with Terraform) or development."""
    pass


@prep.command(name="os")
@pass_ctx
def prep_os(ctx: PyviderContext) -> None:
    """Prepares the operating system with common dependencies."""
    pout(f"🚀 Preparing OS: {ctx.tf_os}", style="cyan bold")

    project_root = Path(__file__).resolve().parent.parent.parent.parent
    script_dir = project_root / "scripts" / "prep" / ctx.tf_os

    if not script_dir.exists() or not script_dir.is_dir():
        perr(f"Error: OS preparation scripts for '{ctx.tf_os}' not found at {script_dir}", style="red bold")
        sys.exit(1)

    scripts = sorted(script_dir.glob("*.sh"))
    for script in scripts:
        title = f"Executing {script.name}"
        try:
            _run_command(["bash", str(script)], check=True, title=title)
        except subprocess.CalledProcessError:
            perr(f"❌ Failed to execute script: {script.name}. Aborting.", style="red bold")
            sys.exit(1)

    pout("✅ OS preparation successfully completed.", style="green bold")


@prep.command(name="terraform")
@pass_ctx
def prep_terraform(ctx: PyviderContext) -> None:
    """Installs Terraform using the appropriate OS-specific script."""
    pout("🚀 Installing Terraform...", style="cyan bold")

    project_root = Path(__file__).resolve().parent.parent.parent.parent

    if ctx.tf_os == "linux":
        script_path = project_root / "scripts" / "prep" / "linux" / "03_install_terraform.sh"
    elif ctx.tf_os == "darwin":
        script_path = project_root / "scripts" / "prep" / "macos" / "04_install_terraform.sh"
    else:
        perr(f"❌ Unsupported OS: {ctx.tf_os}", style="red bold")
        sys.exit(1)

    if not script_path.exists():
        perr(f"❌ Terraform install script not found: {script_path}", style="red bold")
        sys.exit(1)

    try:
        _run_command(
            ["bash", str(script_path)],
            check=True,
            title=f"Installing Terraform for {ctx.tf_os}",
        )
        pout("✅ Terraform installation complete.", style="green bold")
    except subprocess.CalledProcessError:
        perr("❌ Failed to install Terraform. Aborting.", style="red bold")
        sys.exit(1)


@prep.command(name="tofu")
@pass_ctx
def prep_tofu(ctx: PyviderContext) -> None:
    """Installs OpenTofu using the appropriate OS-specific script."""
    pout("🚀 Installing OpenTofu...", style="cyan bold")

    project_root = Path(__file__).resolve().parent.parent.parent.parent

    if ctx.tf_os == "linux":
        script_path = project_root / "scripts" / "prep" / "linux" / "04_install_tofu.sh"
    elif ctx.tf_os == "darwin":
        script_path = project_root / "scripts" / "prep" / "macos" / "05_install_tofu.sh"
    else:
        perr(f"❌ Unsupported OS: {ctx.tf_os}", style="red bold")
        sys.exit(1)

    if not script_path.exists():
        perr(f"❌ OpenTofu install script not found: {script_path}", style="red bold")
        sys.exit(1)

    try:
        _run_command(
            ["bash", str(script_path)],
            check=True,
            title=f"Installing OpenTofu for {ctx.tf_os}",
        )
        pout("✅ OpenTofu installation complete.", style="green bold")
    except subprocess.CalledProcessError:
        perr("❌ Failed to install OpenTofu. Aborting.", style="red bold")
        sys.exit(1)


@prep.command(name="provider")
@pass_ctx
def prep_provider(ctx: PyviderContext) -> None:
    """Prepares Pyvider to be used as a Terraform provider by placing the provider script."""
    click.secho("🔗 Placing Pyvider Terraform provider script...", fg="cyan", bold=True)
    try:
        _place_terraform_provider_script(ctx)
        click.secho("✅ Terraform provider script placement complete.", fg="green")
    except Exception as e:
        click.secho(f"❌ Failed to place Terraform provider script: {e}", fg="red", bold=True)
        sys.exit(1)


@prep.command(name="dev")
@pass_ctx
def prep_dev(ctx: PyviderContext) -> None:
    """Sets up a Python virtual environment in the current directory for development."""
    click.secho("🛠️  Setting up Python development environment...", fg="green", bold=True)
    project_root = Path.cwd()

    if not (project_root / "pyproject.toml").exists():
        click.secho(f"Error: No 'pyproject.toml' found in {project_root}.", fg="red", bold=True)
        sys.exit(1)

    try:
        _run_command(["uv", "venv"], cwd=project_root, title="Creating virtual environment")
        _run_command(
            ["uv", "sync", "--all-groups", "--dev"],
            cwd=project_root,
            title="Syncing dependencies",
        )
        _run_command(
            ["uv", "pip", "install", "-e", "."],
            cwd=str(project_root),
            title="Installing project in editable mode",
        )
        click.secho("\n✅ Development environment setup complete.", fg="green", bold=True)
        click.secho("   Run 'source .venv/bin/activate' to activate it.", fg="yellow")
    except Exception as e:
        click.secho(f"❌ Failed during development setup: {e}", fg="red", bold=True)
        sys.exit(1)


@prep.command(name="all")
@click.pass_context
def prep_all(click_ctx: click.Context) -> None:
    """Runs all preparation steps: os and terraform."""
    click.secho("🚀 Running all preparation steps...", fg="cyan", bold=True)
    click_ctx.invoke(prep_os)
    click.echo("\n--- 🔗 Step 2: Preparing Terraform Provider ---")
    click_ctx.invoke(prep_terraform)
    click.secho("\n🎉 All preparation steps completed successfully!", fg="green", bold=True)
