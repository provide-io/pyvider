#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A log record written inside `CliRunner.invoke` must not swallow the output.

`log_cli = true` puts pytest's live-log handler on the stdlib root logger, and
that handler suspends global capture around every record it writes. pytest's
`SysCaptureBase.suspend`/`resume` hand back the stream pytest recorded when
capture started rather than the one actually installed, so
`CliRunner.isolation()` -- which swaps `sys.stdout` after capture is already
running -- owns a stream pytest has no record of and loses the swap on the first
record. Everything the command prints from then on lands in pytest's own buffer:
`result.output` comes back empty while the command ran correctly and its text
appears under "Captured stdout call".

`provide-testkit`'s pytest plugin patches those two methods to give back the
stream that was in place, which makes the floor on `provide-testkit` in
`pyproject.toml` a correctness dependency rather than a convenience. Run this
file with `-p no:provide_testkit` and the two subcommand cases fail while the
root one passes.

A module-scope `log = get_logger(__name__)` is what arms this in ordinary code:
the logger is bound when its module is imported, and the records it writes from
inside a command reach the root logger while `CliRunner` owns the stream. The
record here is emitted from `PyviderContext`, which the root group callback
constructs, because what matters is that a record is written at some depth
inside the invocation and not which module writes it. It goes to both the
project logger application code holds and the stdlib logger pytest's live-log
handler listens on; the output has to survive either.

`--help` on the root group is an eager Click option that short-circuits before
the group callback, so nothing is logged and that case holds with or without the
fix. Every subcommand path runs the callback first.
"""

from __future__ import annotations

import importlib
import logging

from click.testing import CliRunner
from provide.foundation import get_logger
import pytest

from pyvider.cli import cli
from pyvider.cli.context import PyviderContext

#: The `pyvider.cli.main` module. The package attribute of that name is the
#: entrypoint function defined in `pyvider/cli/__init__.py`, which shadows it.
cli_main = importlib.import_module("pyvider.cli.main")

#: Bound at import, the way a module under test binds its own logger.
log = get_logger(__name__)

#: Said when the swap is gone. The command itself is fine; only its text is lost.
_LOST = "CliRunner lost its stream swap: the command ran, but result.output is empty"


@pytest.fixture(autouse=True)
def _log_from_inside_the_command(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the root group callback write a log record while it runs."""

    class _LoggingContext(PyviderContext):
        def __init__(self) -> None:
            super().__init__()
            log.warning("pyvider context built inside the invocation")
            logging.getLogger(__name__).warning("pyvider context built inside the invocation")

    monkeypatch.setattr(cli_main, "PyviderContext", _LoggingContext)


class TestHelpTextReachesTheCaller:
    """Each invocation's help text comes back on the stream `CliRunner` owns."""

    def test_the_root_group(self) -> None:
        result = CliRunner().invoke(cli, ["--help"])

        assert "Usage:" in result.output, _LOST

    def test_a_subcommand_group(self) -> None:
        result = CliRunner().invoke(cli, ["config", "--help"])

        assert "Usage:" in result.output, _LOST

    def test_a_leaf_command(self) -> None:
        result = CliRunner().invoke(cli, ["config", "show", "--help"])

        assert "Usage:" in result.output, _LOST


# 🐍🏗️🔚
