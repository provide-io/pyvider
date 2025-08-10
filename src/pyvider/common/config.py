"""
Unified, layered configuration system for the Pyvider framework.
"""

import os
from pathlib import Path
import tomllib
from typing import Any

import attrs

from pyvider.telemetry import logger

_DEFAULT_CONFIG_FILENAME = "pyvider.toml"
_DEFAULT_CONFIG_FILE = Path.cwd() / _DEFAULT_CONFIG_FILENAME


@attrs.define(frozen=True)
class PyviderConfig:
    """
    Loads and provides access to configuration from all sources.
    Priority: Environment Variable > Config File > Default.
    """

    _config_data: dict[str, Any] = attrs.field(factory=dict, init=False)
    _loaded_from_path: Path | None = attrs.field(default=None, init=False)

    def __attrs_post_init__(self) -> None:
        logger.debug("⚙️  Config: Initializing configuration loader...")
        config_path_override_str = os.environ.get("PYVIDER_CONFIG_FILE")
        config_path = (
            Path(config_path_override_str).resolve()
            if config_path_override_str
            else _DEFAULT_CONFIG_FILE
        )

        logger.debug("⚙️  Config: Attempting to load from", path=str(config_path))
        if config_path.exists() and config_path.is_file():
            try:
                with config_path.open("rb") as f:
                    config_data = tomllib.load(f)
                    object.__setattr__(self, "_config_data", config_data)
                    object.__setattr__(self, "_loaded_from_path", config_path)
                    logger.debug(
                        "⚙️  Config: Successfully loaded",
                        path=str(config_path),
                        keys=list(config_data.keys()),
                    )
            except (tomllib.TOMLDecodeError, OSError) as e:
                logger.warning(
                    "⚙️  Config: Failed to load config file",
                    path=str(config_path),
                    error=e,
                )
        else:
            logger.debug("⚙️  Config: No config file found", path=str(config_path))

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a configuration value from the highest priority source."""
        logger.debug(f"⚙️  Config: Requesting key '{key}'")

        env_var_name = f"PYVIDER_{key.upper()}"
        if (env_val := os.environ.get(env_var_name)) is not None:
            logger.debug(
                f"⚙️  Config: Found value for '{key}' in environment variable",
                source=env_var_name,
                value=env_val,
            )
            return env_val

        # TOML config keys are nested (e.g., logging.level). We need to handle this.
        key_parts = key.split(".")
        value = self._config_data
        for part in key_parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
                break

        if value is not None:
            logger.debug(
                f"⚙️  Config: Found value for '{key}' in config file",
                source=str(self._loaded_from_path),
                value=value,
            )
            return value

        logger.debug(
            f"⚙️  Config: Using default value for '{key}'", default_value=default
        )
        return default

    @property
    def loaded_file_path(self) -> Path | None:
        return self._loaded_from_path
