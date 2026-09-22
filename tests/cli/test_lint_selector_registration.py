#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for publishing the startup lint selector."""

from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from pyvider.common.config import PyviderConfig
from pyvider.hub import hub
from pyvider.lint import LintSelector


@pytest.fixture
def clean_lint_selector() -> Iterator[None]:
    previous = hub.get_component("singleton", "lint_selector")
    if previous is not None:
        hub.unregister("singleton", "lint_selector")
    try:
        yield
    finally:
        current = hub.get_component("singleton", "lint_selector")
        if current is not None:
            hub.unregister("singleton", "lint_selector")
        if previous is not None:
            hub.register("singleton", "lint_selector", previous)


@pytest.mark.asyncio
async def test_register_runtime_config_publishes_selector_before_server_start(
    monkeypatch: pytest.MonkeyPatch, clean_lint_selector: None
) -> None:
    from pyvider.cli import provide_command
    import pyvider.common.config as config_module

    config = SimpleNamespace(lint_rules=("provide-io/pyvider:security",))
    observed: list[Any] = []

    class StopStartup(Exception):
        pass

    def observe_after_config(_config: object) -> None:
        observed.append(hub.get_component("singleton", "lint_selector"))
        raise StopStartup

    monkeypatch.setattr(config_module, "PyviderConfig", lambda: config)
    monkeypatch.setattr(provide_command, "_configure_telemetry", observe_after_config)
    monkeypatch.setattr(provide_command, "_report_server_crash", observed.append)

    await provide_command._run_provider_server("cookie")

    assert observed[0] == LintSelector.parse(config.lint_rules)
    assert isinstance(observed[1], StopStartup)


def test_register_runtime_config_empty_environment_replaces_earlier_selector(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, clean_lint_selector: None
) -> None:
    from pyvider.cli.provide_command import _register_runtime_config

    hub.register("singleton", "lint_selector", LintSelector(include=frozenset({"all"})))
    monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(tmp_path / "absent.toml"))
    monkeypatch.setenv("PYVIDER_LINT", "")

    _register_runtime_config(PyviderConfig())

    assert hub.get_component("singleton", "lint_selector") == LintSelector()


# 🐍🏗️🔚
