#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from pathlib import Path
from typing import Any

import click
from provide.foundation.context import CLIContext
from provide.foundation.platform import get_arch_name, get_os_name

from pyvider.common.config import PyviderConfig


def _read_version_from_file() -> str:
    """
    Read version from VERSION file in current directory.

    Returns:
        Version string from VERSION file, or "0.0.0" if not found
    """
    version_file = Path.cwd() / "VERSION"
    if version_file.exists():
        try:
            return version_file.read_text().strip()
        except Exception:
            pass
    return "0.0.0"


# --- Pyvider Context Class ---
class PyviderContext(CLIContext):
    """
    Pyvider-specific context that extends foundation's CLIContext.

    Inherits debug, log_level, and other CLI settings from foundation CLIContext.
    """

    def __init__(self) -> None:
        super().__init__()  # Initialize foundation CLIContext
        self.config = PyviderConfig()
        self.home = Path.home()
        self.local_bin_dir = self.home / ".local" / "bin"
        self.tf_os = get_os_name()
        self.tf_arch = get_arch_name()
        self.pyvider_version = _read_version_from_file()
        # Read provider name from config, default to "pyvider" for backwards compatibility
        self.provider_name = self.config.get("pyvider.name", "pyvider")
        self.tf_plugin_dir = (
            self.home
            / ".terraform.d"
            / "plugins"
            / "local"
            / "providers"
            / self.provider_name
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

# 🐍🏗️🔚
