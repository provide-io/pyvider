#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import os
from pathlib import Path
from typing import Any

import click
from provide.foundation import logger
from provide.foundation.context import CLIContext
from provide.foundation.platform import get_arch_name, get_os_name

from pyvider.common.config import PyviderConfig


def _read_provider_name_from_pyproject() -> str | None:
    """
    Read provider_name from pyproject.toml's [tool.pyvider] section.

    Returns:
        Provider name string if found, None otherwise
    """
    pyproject_path = Path.cwd() / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    try:
        # Use tomllib (Python 3.11+) for TOML parsing
        import tomllib

        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)

        # Check [tool.pyvider].provider_name
        tool_pyvider = data.get("tool", {}).get("pyvider", {})
        if "provider_name" in tool_pyvider:
            return str(tool_pyvider["provider_name"])

        # Also check [pyvider].provider_name for consistency
        pyvider_section = data.get("pyvider", {})
        if "provider_name" in pyvider_section:
            return str(pyvider_section["provider_name"])

    except Exception:
        pass  # nosec B110 - intentionally silencing parse errors

    return None


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
            pass  # nosec B110 - intentionally silencing read errors
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
        # Read provider name with priority: env var > pyproject.toml > default
        self.provider_name = self._resolve_provider_name()
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

    def _resolve_provider_name(self) -> str:
        """
        Resolve provider name with priority chain.

        Priority:
        1. Environment variable PYVIDER_PROVIDER_NAME
        2. PYVIDER_CONFIG_FILE (pyvider.toml) [pyvider].name
        3. pyproject.toml [tool.pyvider].provider_name
        4. Default "pyvider" (with warning)

        Returns:
            Resolved provider name
        """
        # 1. Check environment variable first (highest priority)
        env_name = os.environ.get("PYVIDER_PROVIDER_NAME")
        if env_name:
            logger.debug(
                "Provider name from environment variable",
                provider_name=env_name,
                source="PYVIDER_PROVIDER_NAME",
            )
            return env_name

        # 2. Check PYVIDER_CONFIG_FILE (pyvider.toml)
        config_file_path = os.environ.get("PYVIDER_CONFIG_FILE")
        if config_file_path:
            config_name = self._read_provider_name_from_config_file(config_file_path)
            if config_name:
                logger.debug(
                    "Provider name from config file",
                    provider_name=config_name,
                    source=config_file_path,
                )
                return config_name

        # 3. Check pyproject.toml [tool.pyvider].provider_name
        pyproject_name = _read_provider_name_from_pyproject()
        if pyproject_name:
            logger.debug(
                "Provider name from pyproject.toml",
                provider_name=pyproject_name,
                source="pyproject.toml",
            )
            return pyproject_name

        # 4. Fall back to default with warning
        default_name = "pyvider"
        logger.warning(
            "No provider_name configured, using default",
            provider_name=default_name,
            hint="Set provider_name in pyproject.toml under [tool.pyvider] section",
        )
        return default_name

    def _read_provider_name_from_config_file(self, config_file_path: str) -> str | None:
        """Read provider name from a TOML config file (pyvider.toml)."""
        try:
            config_path = Path(config_file_path)
            if not config_path.exists():
                return None
            with config_path.open("rb") as f:
                import tomllib

                data = tomllib.load(f)
            pyvider_section = data.get("pyvider", {})
            if isinstance(pyvider_section, dict):
                name = pyvider_section.get("name")
                if isinstance(name, str):
                    return name
            return None
        except Exception:
            return None

    async def _ensure_components_discovered(
        self,
        registry_obj: Any,
        component_discovery_cls: Any,
        _click_echo_func: Any,
        _click_secho_func: Any,
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
