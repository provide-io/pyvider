#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from collections.abc import Iterator
import os
from pathlib import Path
from typing import Any

import click
from provide.foundation import logger
from provide.foundation.context import CLIContext
from provide.foundation.platform import get_arch_name, get_os_name

from pyvider.common.config import _DEFAULT_CONFIG_FILENAME, PyviderConfig

#: Accepted spellings for the provider-name key, canonical first. The table is
#: already scoped to pyvider, so `name` says everything `provider_name` does;
#: the alias is still read because the docs and one shipped provider spell it
#: that way, and a name that silently does not apply is the worst outcome here.
_PROVIDER_NAME_KEYS = ("name", "provider_name")

#: Used when nothing configures a name. Only correct for one repository in the
#: world, which is why `install` says out loud when it had to fall back.
_DEFAULT_PROVIDER_NAME = "pyvider"


def _load_toml(path: Path) -> dict[str, Any]:
    """Parse a TOML file, returning an empty mapping if it is absent or broken.

    A malformed pyproject.toml must not take the whole CLI down; the caller
    falls through to the next candidate location instead.
    """
    if not path.is_file():
        return {}
    try:
        import tomllib

        with path.open("rb") as f:
            data = tomllib.load(f)
    except Exception:
        return {}  # nosec B110 - unreadable config falls through to the next source
    return data if isinstance(data, dict) else {}


def _name_from_section(section: Any) -> str | None:
    """Pull a provider name out of one config table, canonical key first."""
    if not isinstance(section, dict):
        return None
    for key in _PROVIDER_NAME_KEYS:
        value = section.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _read_provider_name_from_pyproject() -> str | None:
    """
    Read the provider name from pyproject.toml.

    Checks `[tool.pyvider]` -- the PEP 518 location -- before the top-level
    `[pyvider]` table that plating also reads.

    Returns:
        Provider name string if found, None otherwise
    """
    data = _load_toml(Path.cwd() / "pyproject.toml")
    tool_section = data.get("tool")
    scoped = tool_section.get("pyvider") if isinstance(tool_section, dict) else None
    return _name_from_section(scoped) or _name_from_section(data.get("pyvider"))


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
        # Read provider name with priority: env var > pyvider.toml > pyproject.toml
        self.provider_name, self.provider_name_source = self._resolve_provider_name()
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

    def _provider_name_candidates(self) -> Iterator[tuple[str | None, str]]:
        """
        Yield (name, source) pairs in resolution order, highest priority first.

        A pair whose name is None or empty means "this location did not
        configure a name"; the caller moves on to the next one.
        """
        yield os.environ.get("PYVIDER_PROVIDER_NAME"), "PYVIDER_PROVIDER_NAME"

        # An explicitly pointed-at config file outranks project metadata.
        config_file_path = os.environ.get("PYVIDER_CONFIG_FILE")
        if config_file_path:
            yield (
                self._read_provider_name_from_config_file(config_file_path),
                f"{config_file_path} [pyvider]",
            )

        # PyviderConfig already loads pyvider.toml from the cwd by default, so
        # the name in it must be honoured there too -- requiring
        # PYVIDER_CONFIG_FILE to see it made the file's own `[pyvider] name`
        # inert in every normal checkout.
        yield (
            self._read_provider_name_from_config_file(_DEFAULT_CONFIG_FILENAME),
            f"{_DEFAULT_CONFIG_FILENAME} [pyvider]",
        )

        pyproject = _load_toml(Path.cwd() / "pyproject.toml")
        tool_section = pyproject.get("tool")
        scoped = tool_section.get("pyvider") if isinstance(tool_section, dict) else None
        yield _name_from_section(scoped), "pyproject.toml [tool.pyvider]"
        # Top-level `[pyvider]` is not a PEP 518 location, but plating reads it
        # and providers in the wild write it, so it is accepted last.
        yield _name_from_section(pyproject.get("pyvider")), "pyproject.toml [pyvider]"

    def _resolve_provider_name(self) -> tuple[str, str]:
        """
        Resolve the provider name and record where it came from.

        Priority:
        1. Environment variable PYVIDER_PROVIDER_NAME
        2. PYVIDER_CONFIG_FILE, `[pyvider]`
        3. ./pyvider.toml, `[pyvider]`
        4. ./pyproject.toml, `[tool.pyvider]`
        5. ./pyproject.toml, `[pyvider]`
        6. Default "pyvider" (with a warning)

        Either `name` or `provider_name` is accepted as the key in any of them.

        Returns:
            (resolved name, human-readable description of its source)
        """
        for name, source in self._provider_name_candidates():
            if name:
                logger.debug("Provider name resolved", provider_name=name, source=source)
                return name, source

        logger.warning(
            "No provider name configured, using default",
            provider_name=_DEFAULT_PROVIDER_NAME,
            hint='Set name = "<provider>" in pyproject.toml under [tool.pyvider]',
        )
        return _DEFAULT_PROVIDER_NAME, "default"

    def _read_provider_name_from_config_file(self, config_file_path: str) -> str | None:
        """Read the provider name from a TOML config file (pyvider.toml)."""
        data = _load_toml(Path(config_file_path))
        return _name_from_section(data.get("pyvider"))

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
