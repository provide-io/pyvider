"""
Unified, layered configuration system for the Pyvider framework.
"""

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
        validator=validate_choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
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
        logger.debug("⚙️  Config: Initializing configuration loader...")
        config_path_override_str = os.environ.get("PYVIDER_CONFIG_FILE")
        config_path = (
            Path(config_path_override_str).resolve() if config_path_override_str else _DEFAULT_CONFIG_FILE
        )

        logger.debug("⚙️  Config: Attempting to load from", path=str(config_path))
        try:
            config_data = read_toml(config_path)
            if config_data:  # Only set if file exists and has content
                object.__setattr__(self, "_config_data", config_data)
                object.__setattr__(self, "_loaded_from_path", config_path)
                logger.debug(
                    "⚙️  Config: Successfully loaded",
                    path=str(config_path),
                    keys=list(config_data.keys()),
                )
        except Exception as e:
            logger.warning(
                "⚙️  Config: Failed to load config file",
                path=str(config_path),
                error=e,
            )
        else:
            logger.debug("⚙️  Config: No config file found", path=str(config_path))

        # Override typed fields with environment variables if present
        self._load_env_overrides()

    def get(self, key: str, default: Any = None) -> Any:
        """Gets a configuration value from the highest priority source."""
        logger.debug(f"⚙️  Config: Requesting key '{key}'")

        # First check if this is a typed field
        from attrs import fields

        for fld in fields(type(self)):
            if fld.name == key and not fld.name.startswith("_"):
                value = getattr(self, key)
                logger.debug(f"⚙️  Config: Found typed field '{key}'", value=value)
                return value

        # Fallback to legacy behavior for dynamic keys
        env_var_name = f"PYVIDER_{key.upper()}"
        if (env_val := get_env(env_var_name)) is not None:
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

        logger.debug(f"⚙️  Config: Using default value for '{key}'", default_value=default)
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
            logger.debug("⚙️  Config: Loaded private_state_shared_secret from environment")

        env_log_level = get_env("PYVIDER_LOG_LEVEL")
        if env_log_level:
            object.__setattr__(self, "log_level", env_log_level.upper())  # Normalize case
            logger.debug("⚙️  Config: Loaded log_level from environment")

        # Load other typed fields
        env_timeout = get_env("PYVIDER_MAX_DISCOVERY_TIMEOUT")
        if env_timeout is not None:
            try:
                timeout_val = int(env_timeout)
                object.__setattr__(self, "max_discovery_timeout", timeout_val)
                logger.debug("⚙️  Config: Loaded max_discovery_timeout from environment")
            except ValueError:
                logger.warning("⚙️  Config: Invalid max_discovery_timeout value, using default")

    def validate_required_fields(self) -> None:
        """Validates that all required fields are properly configured."""
        if not self.private_state_shared_secret:
            raise ConfigurationError(
                "Private state shared secret is required. Set PYVIDER_PRIVATE_STATE_SHARED_SECRET "
                "environment variable or define 'private_state_shared_secret' in your config file."
            )

        logger.debug("⚙️  Config: All required fields validated successfully")
