#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI entrypoint modules."""

import importlib
import inspect

from provide.testkit.mocking import AsyncMock, Mock
import pytest


def _drain_coroutine(mock_run: Mock) -> None:
    """Ensure mocked coroutines are closed to avoid warnings."""
    (coro,) = mock_run.call_args.args
    if inspect.iscoroutine(coro):
        coro.close()


def test_cli_main_invokes_cli_and_shutdown(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure the CLI entrypoint delegates to click and cleans up Foundation."""
    import pyvider.cli.__main__ as cli_entrypoint

    mock_cli = Mock()
    monkeypatch.setattr(cli_entrypoint, "cli", mock_cli)

    mock_shutdown = AsyncMock(return_value=None)
    monkeypatch.setattr(cli_entrypoint, "shutdown_foundation", mock_shutdown)

    mock_run = Mock()
    monkeypatch.setattr(cli_entrypoint.asyncio, "run", mock_run)

    cli_entrypoint.main()

    mock_cli.assert_called_once_with()
    mock_shutdown.assert_called_once_with()
    mock_run.assert_called_once()
    _drain_coroutine(mock_run)


def test_cli_main_ensures_shutdown_on_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Even when the click command fails, the shutdown routine must run."""
    import pyvider.cli.__main__ as cli_entrypoint

    mock_cli = Mock(side_effect=RuntimeError("boom"))
    monkeypatch.setattr(cli_entrypoint, "cli", mock_cli)

    mock_shutdown = AsyncMock(return_value=None)
    monkeypatch.setattr(cli_entrypoint, "shutdown_foundation", mock_shutdown)

    mock_run = Mock()
    monkeypatch.setattr(cli_entrypoint.asyncio, "run", mock_run)

    with pytest.raises(RuntimeError):
        cli_entrypoint.main()

    mock_shutdown.assert_called_once_with()
    mock_run.assert_called_once()
    _drain_coroutine(mock_run)


def test_package_main_aliases_cli_main() -> None:
    """The package-level __main__ module should expose the CLI entrypoint."""
    cli_entrypoint = importlib.import_module("pyvider.cli.__main__")
    package_entrypoint = importlib.import_module("pyvider.__main__")

    assert package_entrypoint.main is cli_entrypoint.main


# 🐍🏗️🔚
