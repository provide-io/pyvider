#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unified, layered configuration system for the Pyvider framework."""

import os
from pathlib import Path
from typing import Any

from attrs import define, field as attrs_field
from provide.foundation import logger
from provide.foundation.config import (
    BaseConfig,
    ConfigError as ConfigurationError,
    field,
    get_env,
    validate_choice,
    validate_positive,
)
from provide.foundation.file import read_toml

_DEFAULT_CONFIG_FILENAME = "pyvider.toml"
_DEFAULT_CONFIG_FILE = Path.cwd() / _DEFAULT_CONFIG_FILENAME
_SOUP_CONFIG_FILE = Path.cwd() / "soup.toml"


@define(frozen=True)
class PyviderConfig(BaseConfig):
    """
    Enhanced configuration system with validation and type safety.
    Priority: Environment Variable > Config File > Default.

    Uses provide.foundation's advanced configuration features.
    """

    # Core configuration fields with validation
    log_level: str = field(
        default="INFO",
        validator=validate_choice(["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
        description="Logging level for the application",
        env_var="PYVIDER_LOG_LEVEL",
    )

    config_file_path: str = field(
        default="pyvider.toml", description="Path to the configuration file", env_var="PYVIDER_CONFIG_FILE"
    )

    private_state_shared_secret: str = field(
        default="",
        description="Shared secret for private state encryption",
        env_var="PYVIDER_PRIVATE_STATE_SHARED_SECRET",
        sensitive=True,
    )

    max_discovery_timeout: int = field(
        default=30,
        validator=validate_positive,
        description="Maximum timeout for component discovery in seconds",
        env_var="PYVIDER_MAX_DISCOVERY_TIMEOUT",
    )

    # Legacy support for the custom loading logic
    _config_data: dict[str, Any] = attrs_field(factory=dict, init=False)
    _loaded_from_path: Path | None = attrs_field(default=None, init=False)

    def __attrs_post_init__(self) -> None:
        logger.debug(
            "Configuration loader initializing",
            operation="config_init",
        )

        config_path_override_str = os.environ.get("PYVIDER_CONFIG_FILE")
        if config_path_override_str:
            config_path = Path(config_path_override_str).resolve()
        elif _DEFAULT_CONFIG_FILE.exists():
            config_path = _DEFAULT_CONFIG_FILE
        elif _SOUP_CONFIG_FILE.exists():
            config_path = _SOUP_CONFIG_FILE
        else:
            config_path = _DEFAULT_CONFIG_FILE  # Use default for error message

        logger.debug(
            "Attempting to load configuration file",
            operation="config_load",
            config_path=str(config_path),
            is_override=bool(config_path_override_str),
        )

        try:
            config_data = read_toml(config_path)
            if config_data:  # Only set if file exists and has content
                object.__setattr__(self, "_config_data", config_data)
                object.__setattr__(self, "_loaded_from_path", config_path)
                logger.info(
                    "Configuration file loaded successfully",
                    operation="config_load",
                    config_path=str(config_path),
                    config_keys=list(config_data.keys()),
                    key_count=len(config_data),
                )
        except Exception as e:
            logger.warning(
                "Failed to load configuration file, using defaults",
                operation="config_load",
                config_path=str(config_path),
                error_type=type(e).__name__,
                error_message=str(e),
            )
        else:
            logger.debug(
                "No configuration file found, using defaults",
                operation="config_load",
                searched_path=str(config_path),
            )

        # Override typed fields with environment variables if present
        logger.debug(
            "Loading environment variable overrides",
            operation="config_env_override",
        )
        self._load_env_overrides()

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a configuration value from the highest priority source."""

        # First check if this is a typed field
        from attrs import fields

        for fld in fields(type(self)):
            if fld.name == key and not fld.name.startswith("_"):
                value = getattr(self, key)
                return value

        # Fallback to legacy behavior for dynamic keys
        env_var_name = f"PYVIDER_{key.upper()}"
        if (env_val := get_env(env_var_name)) is not None:
            logger.debug(
                "Debug info",
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
                "Debug info",
                source=str(self._loaded_from_path),
                value=value,
            )
            return value

        return default

    @property
    def loaded_file_path(self) -> Path | None:
        return self._loaded_from_path

    def _load_env_overrides(self) -> None:
        """Load environment variable overrides for typed fields using foundation's get_env."""
        # Use foundation's enhanced environment variable loading
        env_secret = get_env("PYVIDER_PRIVATE_STATE_SHARED_SECRET")
        if env_secret:
            object.__setattr__(self, "private_state_shared_secret", env_secret)

        env_log_level = get_env("PYVIDER_LOG_LEVEL")
        if env_log_level:
            object.__setattr__(self, "log_level", env_log_level.upper())  # Normalize case

        # Load other typed fields
        env_timeout = get_env("PYVIDER_MAX_DISCOVERY_TIMEOUT")
        if env_timeout is not None:
            try:
                timeout_val = int(env_timeout)
                object.__setattr__(self, "max_discovery_timeout", timeout_val)
            except ValueError:
                pass

    def validate_required_fields(self) -> None:
        """Validates that all required fields are properly configured."""
        if not self.private_state_shared_secret:
            raise ConfigurationError(
                "Private state shared secret is required. Set PYVIDER_PRIVATE_STATE_SHARED_SECRET "
                "environment variable or define 'private_state_shared_secret' in your config file."
            )


# 🐍🏗️🔚
