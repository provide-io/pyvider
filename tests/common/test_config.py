#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for pyvider/common/config.py."""

from pathlib import Path

from provide.foundation.config import ConfigError as ConfigurationError
import pytest

from pyvider.common.config import PyviderConfig


@pytest.fixture(autouse=True)
def clean_log_level_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure PYVIDER_LOG_LEVEL is not set for tests that expect default log level."""
    monkeypatch.delenv("PYVIDER_LOG_LEVEL", raising=False)
    yield


class TestPyviderConfigInitialization:
    """Tests for PyviderConfig initialization."""

    def test_config_defaults(self) -> None:
        """Test that config has sensible defaults."""
        config = PyviderConfig()
        assert config.log_level == "INFO"
        assert config.max_discovery_timeout == 30
        assert config.config_file_path == "pyvider.toml"

    def test_config_env_override_log_level(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that environment variables override defaults for log_level."""
        monkeypatch.setenv("PYVIDER_LOG_LEVEL", "DEBUG")
        config = PyviderConfig()
        assert config.log_level == "DEBUG"

    def test_config_env_override_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that environment variables override defaults for timeout."""
        monkeypatch.setenv("PYVIDER_MAX_DISCOVERY_TIMEOUT", "60")
        config = PyviderConfig()
        assert config.max_discovery_timeout == 60

    def test_config_env_override_secret(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that environment variables override defaults for secret."""
        monkeypatch.setenv("PYVIDER_PRIVATE_STATE_SHARED_SECRET", "test-secret")
        config = PyviderConfig()
        assert config.private_state_shared_secret == "test-secret"

    def test_config_invalid_timeout_value(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that invalid timeout value falls back to default."""
        monkeypatch.setenv("PYVIDER_MAX_DISCOVERY_TIMEOUT", "invalid")
        config = PyviderConfig()
        # Should use default value
        assert config.max_discovery_timeout == 30


class TestPyviderConfigFileLoading:
    """Tests for config file loading."""

    def test_config_loads_from_file(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Test that config loads from TOML file."""
        config_file = tmp_path / "pyvider.toml"
        config_file.write_text("""
[logging]
level = "DEBUG"

[server]
timeout_graceful_shutdown = 10
""")
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))
        config = PyviderConfig()

        # Check that file was loaded
        assert config.loaded_file_path == config_file
        assert config.get("logging.level") == "DEBUG"
        assert config.get("server.timeout_graceful_shutdown") == 10

    def test_config_handles_missing_file(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that config handles missing file gracefully."""
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", "/nonexistent/path/config.toml")
        # Should not raise, just log a warning
        config = PyviderConfig()
        assert config.loaded_file_path is None

    def test_config_handles_invalid_toml(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Test that config handles invalid TOML file."""
        config_file = tmp_path / "invalid.toml"
        config_file.write_text("this is not valid TOML {{{}}")
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))

        # Should not raise, just log a warning
        config = PyviderConfig()
        assert config.loaded_file_path is None


class TestPyviderConfigGet:
    """Tests for config.get() method."""

    def test_get_typed_field(self) -> None:
        """Test getting a typed field."""
        config = PyviderConfig()
        assert config.get("log_level") == "INFO"
        assert config.get("max_discovery_timeout") == 30

    def test_get_with_default(self) -> None:
        """Test get with default value."""
        config = PyviderConfig()
        assert config.get("nonexistent_key", "default_value") == "default_value"

    def test_get_nested_config_value(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Test getting nested config values."""
        config_file = tmp_path / "pyvider.toml"
        config_file.write_text("""
[database]
host = "localhost"
port = 5432

[database.connection]
max_pool_size = 10
""")
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))
        config = PyviderConfig()

        assert config.get("database.host") == "localhost"
        assert config.get("database.port") == 5432
        assert config.get("database.connection.max_pool_size") == 10

    def test_get_env_var_override(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Test that env vars take precedence over config file."""
        config_file = tmp_path / "pyvider.toml"
        config_file.write_text("""
custom_key = "file_value"
""")
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))
        monkeypatch.setenv("PYVIDER_CUSTOM_KEY", "env_value")
        config = PyviderConfig()

        # Env var should take precedence
        assert config.get("custom_key") == "env_value"

    def test_get_handles_non_dict_nested_value(self) -> None:
        """Test that get handles non-dict values in nested lookup."""
        config = PyviderConfig()
        # This should return None, not crash
        result = config.get("log_level.nested.value")
        assert result is None


class TestPyviderConfigValidation:
    """Tests for config validation."""

    def test_validate_required_fields_raises_without_secret(self) -> None:
        """Test that validation raises error when secret is missing."""
        config = PyviderConfig()
        with pytest.raises(ConfigurationError, match="Private state shared secret"):
            config.validate_required_fields()

    def test_validate_required_fields_passes_with_secret(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that validation passes when secret is provided."""
        monkeypatch.setenv("PYVIDER_PRIVATE_STATE_SHARED_SECRET", "test-secret")
        config = PyviderConfig()
        # Should not raise
        config.validate_required_fields()

    def test_log_level_case_normalization(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that log level is normalized to uppercase."""
        monkeypatch.setenv("PYVIDER_LOG_LEVEL", "debug")
        config = PyviderConfig()
        assert config.log_level == "DEBUG"


class TestPyviderConfigProperties:
    """Tests for config properties."""

    def test_loaded_file_path_property(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """Test the loaded_file_path property."""
        config_file = tmp_path / "pyvider.toml"
        config_file.write_text("[test]\nvalue = 123")
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))
        config = PyviderConfig()

        assert config.loaded_file_path == config_file

    def test_loaded_file_path_none_when_no_file(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that loaded_file_path is None when no file loaded."""
        # Point to a non-existent file
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", "/nonexistent/config.toml")
        config = PyviderConfig()
        # With no config file, should be None
        assert config.loaded_file_path is None


# 🐍🏗️🔚
