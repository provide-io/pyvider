#!/usr/bin/env python3
from pathlib import Path
import platform


def get_provider_filename() -> str:
    """Generate the correct provider binary name following Terraform naming convention."""
    # Corrected to 'terraform-provider-pyvider'
    return "terraform-provider-pyvider"


def setup_provider_directory() -> Path:
    """Create the provider directory structure for local/providers/pyvider."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    arch_map = {"x86_64": "amd64", "amd64": "amd64", "arm64": "arm64", "aarch64": "arm64"}
    arch = arch_map.get(machine, machine)
    version = "0.1.0"  # Ensure this matches the version used in provider.tf

    # Corrected path to match 'local/providers/pyvider'
    plugin_dir = (
        Path.home()
        / ".terraform.d"
        / "plugins"
        / "local"
        / "providers"
        / "pyvider"
        / version
        / f"{system}_{arch}"
    )
    plugin_dir.mkdir(parents=True, exist_ok=True)
    return plugin_dir
