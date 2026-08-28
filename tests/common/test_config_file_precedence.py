#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`PyviderConfig` promises "Environment Variable > Config File > Default"."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from provide.foundation.config import ConfigError as ConfigurationError
import pytest

from pyvider.common.config import PyviderConfig


@pytest.fixture
def config_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    path = tmp_path / "pyvider.toml"
    monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(path))
    for leftover in (
        "PYVIDER_PRIVATE_STATE_SHARED_SECRET",
        "PYVIDER_LOG_LEVEL",
        "PYVIDER_MAX_DISCOVERY_TIMEOUT",
    ):
        monkeypatch.delenv(leftover, raising=False)
    yield path


class TestTheFileIsActuallyRead:
    def test_a_secret_in_the_file_reaches_the_typed_field(self, config_file: Path) -> None:
        """docs/schema/sensitive-data.md tells operators to write exactly this."""
        config_file.write_text('private_state_shared_secret = "s3cret-from-toml"\n')

        config = PyviderConfig()

        assert config.private_state_shared_secret == "s3cret-from-toml"
        assert config.get("private_state_shared_secret") == "s3cret-from-toml"

    def test_a_secret_in_the_file_satisfies_the_required_check(self, config_file: Path) -> None:
        """The error told operators to do the thing they had already done."""
        config_file.write_text('private_state_shared_secret = "s3cret-from-toml"\n')

        PyviderConfig().validate_required_fields()  # must not raise

    def test_a_nested_log_level_reaches_the_typed_field(self, config_file: Path) -> None:
        """The shipped pyvider.toml spells it `[logging] level`, not `log_level`."""
        config_file.write_text('[logging]\nlevel = "DEBUG"\n')

        assert PyviderConfig().log_level == "DEBUG"

    def test_a_top_level_spelling_also_works(self, config_file: Path) -> None:
        config_file.write_text('log_level = "ERROR"\n')

        assert PyviderConfig().log_level == "ERROR"

    def test_an_integer_field_is_read(self, config_file: Path) -> None:
        config_file.write_text("max_discovery_timeout = 90\n")

        assert PyviderConfig().max_discovery_timeout == 90


class TestPrecedence:
    def test_the_environment_beats_the_file(self, config_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        config_file.write_text('private_state_shared_secret = "from-toml"\n')
        monkeypatch.setenv("PYVIDER_PRIVATE_STATE_SHARED_SECRET", "from-env")

        assert PyviderConfig().private_state_shared_secret == "from-env"

    def test_the_file_beats_the_default(self, config_file: Path) -> None:
        config_file.write_text('[logging]\nlevel = "TRACE"\n')

        assert PyviderConfig().log_level == "TRACE"

    def test_the_default_stands_when_neither_is_set(self, config_file: Path) -> None:
        config_file.write_text("# empty\n")

        config = PyviderConfig()

        assert config.log_level == "INFO"
        assert config.private_state_shared_secret == ""
        assert config.max_discovery_timeout == 30


class TestBadInputDoesNotBreakStartup:
    def test_an_invalid_choice_is_ignored_rather_than_fatal(self, config_file: Path) -> None:
        """A typo in a config file should not stop the provider from starting."""
        config_file.write_text('[logging]\nlevel = "LOUD"\n')

        assert PyviderConfig().log_level == "INFO"

    def test_a_wrongly_typed_value_is_ignored(self, config_file: Path) -> None:
        config_file.write_text('max_discovery_timeout = "not-a-number"\n')

        assert PyviderConfig().max_discovery_timeout == 30

    def test_a_missing_file_still_yields_defaults(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(tmp_path / "absent.toml"))
        monkeypatch.delenv("PYVIDER_PRIVATE_STATE_SHARED_SECRET", raising=False)

        config = PyviderConfig()

        assert config.log_level == "INFO"
        with pytest.raises(ConfigurationError):
            config.validate_required_fields()


# 🌊🪢🔚
