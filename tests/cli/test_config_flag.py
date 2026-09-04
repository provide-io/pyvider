#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`--config FILE` names a file to read, and the loaded config survives it.

The root group stores every parsed option on the context under its own name.
`--config` carries a path rather than a setting, so that store replaced the
loaded `PyviderConfig` with a `Path`, and the next `ctx.config.<anything>`
raised `AttributeError` -- `pyvider --config x.toml config show` could not run
at all.

The flag is the command-line spelling of `PYVIDER_CONFIG_FILE`, so it is
applied there: the context, the provider-name resolution and `config show`'s
own report of where it looked all read that one variable.
"""

from __future__ import annotations

import os
from pathlib import Path

from click.testing import CliRunner
import pytest

from pyvider.cli import cli
from pyvider.cli.__main__ import _option_from_argv

#: A key `config show` prints verbatim, so the output proves which file was read.
_MARKER = "config-flag-marker"


@pytest.fixture(autouse=True)
def _restore_config_env() -> None:
    """Put `PYVIDER_CONFIG_FILE` back; the code under test creates it."""
    saved = os.environ.get("PYVIDER_CONFIG_FILE")
    yield
    if saved is None:
        os.environ.pop("PYVIDER_CONFIG_FILE", None)
    else:
        os.environ["PYVIDER_CONFIG_FILE"] = saved


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    path = tmp_path / "alternate.toml"
    path.write_text(f'{_MARKER} = "read"\n')
    return path


class TestTheFlagDoesNotReplaceTheConfig:
    def test_config_show_runs(self, config_file: Path) -> None:
        result = CliRunner().invoke(cli, ["--config", str(config_file), "config", "show"])

        assert result.exit_code == 0, f"`--config` broke `config show`: {result.exception!r}"

    def test_the_named_file_is_the_one_read(self, config_file: Path) -> None:
        result = CliRunner().invoke(cli, ["--config", str(config_file), "config", "show"])

        assert _MARKER in result.output, "the file named by `--config` was not the file read"

    def test_the_environment_carries_the_choice(self, config_file: Path) -> None:
        CliRunner().invoke(cli, ["--config", str(config_file), "config", "show"])

        assert os.environ["PYVIDER_CONFIG_FILE"] == str(config_file)

    def test_the_variable_is_left_alone_without_the_flag(self) -> None:
        before = os.environ.get("PYVIDER_CONFIG_FILE")

        CliRunner().invoke(cli, ["config", "show"])

        assert os.environ.get("PYVIDER_CONFIG_FILE") == before, (
            "the flag's default was applied as though the flag had been given"
        )


class TestTheFlagIsReadBeforeFoundationStarts:
    """Telemetry is configured from a `PyviderConfig` built before Click parses."""

    def test_a_separate_value_is_found(self) -> None:
        assert _option_from_argv(["pyvider", "--config", "a.toml"], "--config") == "a.toml"

    def test_an_equals_form_is_found(self) -> None:
        assert _option_from_argv(["pyvider", "--config=a.toml"], "--config") == "a.toml"

    def test_absence_is_reported_as_none(self) -> None:
        assert _option_from_argv(["pyvider", "provide"], "--config") is None

    def test_a_trailing_flag_with_no_value_is_not_a_crash(self) -> None:
        assert _option_from_argv(["pyvider", "--config"], "--config") is None


# 🐍🏗️🔚
