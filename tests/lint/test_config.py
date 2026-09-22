#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for lint selector configuration precedence."""

from pathlib import Path
from unittest.mock import patch

import pytest

from pyvider.common.config import PyviderConfig


@pytest.fixture(autouse=True)
def clean_lint_environment(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("PYVIDER_LINT", raising=False)
    monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(tmp_path / "absent.toml"))


def test_lint_config_defaults_to_disabled() -> None:
    assert PyviderConfig().lint_rules == ()


def test_lint_config_reads_toml_rules(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config_file = tmp_path / "pyvider.toml"
    config_file.write_text('[lint]\nrules = ["file-rule", "!file-excluded"]\n')
    monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))

    assert PyviderConfig().lint_rules == ("file-rule", "!file-excluded")


def test_lint_config_environment_rules_override_toml(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config_file = tmp_path / "pyvider.toml"
    config_file.write_text('[lint]\nrules = ["file-rule"]\n')
    monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))
    monkeypatch.setenv("PYVIDER_LINT", "env-rule,!env-excluded")

    assert PyviderConfig().lint_rules == ("env-rule", "!env-excluded")


def test_lint_config_empty_environment_disables_toml(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config_file = tmp_path / "pyvider.toml"
    config_file.write_text('[lint]\nrules = ["file-rule"]\n')
    monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))
    monkeypatch.setenv("PYVIDER_LINT", "")

    assert PyviderConfig().lint_rules == ()


def test_lint_config_malformed_entries_are_ignored(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config_file = tmp_path / "pyvider.toml"
    config_file.write_text('[lint]\nrules = [" valid-rule ", 3, "Uppercase", "!valid-excluded"]\n')
    monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))

    assert PyviderConfig().lint_rules == ("valid-rule", "!valid-excluded")


def test_lint_config_wrong_toml_rules_type_logs_and_disables(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config_file = tmp_path / "pyvider.toml"
    config_file.write_text('[lint]\nrules = "all"\n')
    monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(config_file))

    with patch("pyvider.common.config.logger.warning") as warning:
        config = PyviderConfig()

    assert config.lint_rules == ()
    warning.assert_called_once()
    assert warning.call_args.kwargs["operation"] == "lint_config_load"


# 🐍🏗️🔚
