import pathlib
import platform
import sys
from typing import Any

import click

from pyvider.common.config import PyviderConfig


# --- Module-level helper functions for Terraform OS/Arch ---
def terraform_arch() -> str:
    machine = platform.machine().lower()
    match machine:
        case "x86_64":
            return "amd64"
        case "aarch64" | "arm64":
            return "arm64"
        case _:
            return "unknown_arch"


def terraform_os() -> str:
    os_name = sys.platform
    if os_name.startswith("linux"):
        return "linux"
    if os_name == "darwin":
        return "darwin"
    if os_name in ("win32", "cygwin"):
        return "windows"
    return "unknown_os"


# --- Pyvider Context Class ---
class PyviderContext:
    def __init__(self) -> None:
        self.config = PyviderConfig()
        self.home = pathlib.Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = terraform_os()
        self.tf_arch = terraform_arch()
        self.pyvider_version = self.config.get("version", "0.1.0")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / "pyvider"
            / self.pyvider_version
            / f"{self.tf_os}_{self.tf_arch}"
        )
        self.components_discovered = False
        self.discovery_errors: list[tuple[str, Exception]] = []

    async def _ensure_components_discovered(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        click_echo_func: Any,
        click_secho_func: Any,
    ) -> None:
        if not self.components_discovered:
            try:
                discovery = component_discovery_cls(registry_obj)
                # THE FIX: Run discovery in non-strict mode to capture all errors
                await discovery.discover_all(strict=False)
                self.discovery_errors = discovery.import_errors
                self.components_discovered = True
            except Exception as e:
                # Capture unexpected errors during the discovery process itself
                self.discovery_errors.append(("discovery_runner", e))
                self.components_discovered = False


pass_ctx = click.make_pass_decorator(PyviderContext, ensure=True)
