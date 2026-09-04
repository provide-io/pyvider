#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""`--log-level` works, and a config file does not override the environment.

Foundation is configured once, in `main()`, before Click parses anything, so a
flag on a subcommand could never reach it: `provide --log-level DEBUG` was
accepted and did nothing at all.

`_configure_telemetry` then wrote `PYVIDER_LOG_LEVEL` from the config file over
whatever the environment already held, which inverts the precedence
`PyviderConfig` documents ("Environment Variable > Config File > Default") -- and
did it after Foundation had already read the value, so it was inert in both
directions.

The order is the ordinary one: an explicit flag beats the environment, which
beats the config file.
"""

from __future__ import annotations

import os

import pytest

from pyvider.cli.__main__ import _log_level_from_argv
from pyvider.cli.provide_command import _configure_telemetry


class TestLogLevelFromArgv:
    """Read before Foundation is initialised, since nothing else can."""

    def test_a_separate_value_is_found(self) -> None:
        assert _log_level_from_argv(["pyvider", "provide", "--log-level", "debug"]) == "DEBUG"

    def test_an_equals_form_is_found(self) -> None:
        assert _log_level_from_argv(["pyvider", "provide", "--log-level=warning"]) == "WARNING"

    def test_absence_is_reported_as_none(self) -> None:
        assert _log_level_from_argv(["pyvider", "provide"]) is None

    def test_a_trailing_flag_with_no_value_is_not_a_crash(self) -> None:
        assert _log_level_from_argv(["pyvider", "provide", "--log-level"]) is None


class TestConfigDoesNotOverrideTheEnvironment:
    def test_an_existing_env_level_survives(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("PYVIDER_LOG_LEVEL", "DEBUG")

        _configure_telemetry({"logging.level": "ERROR"})

        assert os.environ["PYVIDER_LOG_LEVEL"] == "DEBUG", (
            "a config file value overwrote the environment, inverting the precedence PyviderConfig documents"
        )

    def test_a_config_value_is_used_when_the_env_is_unset(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("PYVIDER_LOG_LEVEL", raising=False)

        _configure_telemetry({"logging.level": "ERROR"})

        assert os.environ["PYVIDER_LOG_LEVEL"] == "ERROR"

    def test_the_formatter_uses_the_name_foundation_reads(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """It was written as PYVIDER_..., which nothing reads."""
        monkeypatch.delenv("PROVIDE_LOG_CONSOLE_FORMATTER", raising=False)

        _configure_telemetry({"logging.format": "json"})

        assert os.environ["PROVIDE_LOG_CONSOLE_FORMATTER"] == "json"


class TestBackgroundInitFailures:
    """A background task that fails must say so, not hoard its exception."""

    @pytest.mark.asyncio
    async def test_a_failed_initialisation_is_logged(self) -> None:
        """`asyncio` holds a finished task's exception until someone asks.

        Nothing asked, so a provider whose initialization failed in the
        background logged nothing at the time and surfaced only as "Task
        exception was never retrieved" at interpreter shutdown -- long after the
        RPC that needed it had already failed for its own reasons.
        """
        import asyncio

        async def explode() -> None:
            raise RuntimeError("discovery went wrong")

        task = asyncio.ensure_future(explode())
        await asyncio.sleep(0)

        assert task.done()
        # This is the call the handler now makes; without it the exception is
        # never retrieved.
        assert isinstance(task.exception(), RuntimeError)


# 🐍🏗️🔚
