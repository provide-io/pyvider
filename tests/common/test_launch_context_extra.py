#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests for launch context helpers covering edge scenarios."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import ModuleType
from typing import Never

import pytest

import pyvider.common.launch_context as lc
from pyvider.common.launch_context import (
    LaunchContext,
    LaunchMethod,
    _analyze_cache_structure,
    _analyze_executable,
    _get_editable_install_details,
    detect_launch_context,
    log_launch_context,
)


def test_detect_launch_context_without_terraform_cookie(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delitem(lc.os.environ, "TF_PLUGIN_MAGIC_COOKIE", raising=False)
    monkeypatch.setattr(lc.sys, "argv", ["/bin/pyvider"])
    monkeypatch.setattr(lc.sys, "executable", "/usr/bin/python3")
    monkeypatch.setattr(lc.sys, "version", "3.x-test")
    monkeypatch.setattr(lc.sys, "platform", "posix")
    monkeypatch.setattr(lc.sys, "path", ["a", "b"])
    monkeypatch.setattr(lc.os, "getcwd", lambda: "/tmp")
    monkeypatch.setattr(lc, "_detect_launch_method", lambda exe, py: (LaunchMethod.UNKNOWN, {}))

    context = detect_launch_context()

    assert context.is_terraform_invoked is False
    assert context.environment_info["terraform_cookie_present"] is False


def test_get_editable_install_details_reports_development_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    dummy_module = ModuleType("pyvider")
    dummy_module.__file__ = "/repo/src/pyvider/__init__.py"
    dummy_module.__path__ = ["/repo/src/pyvider"]
    monkeypatch.setitem(lc.sys.modules, "pyvider", dummy_module)

    details = _get_editable_install_details("/repo/.venv/bin/pyvider")

    assert details["pyvider_location"].endswith("src")
    assert details["is_development_mode"] is True


def test_analyze_executable_reports_missing(tmp_path: Path) -> None:
    missing = tmp_path / "missing.py"
    info = _analyze_executable(str(missing))
    assert info["exists"] is False
    assert info["is_file"] is False


def test_analyze_cache_structure_handles_errors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    python_path = tmp_path / "venv" / "bin" / "python"
    python_path.parent.mkdir(parents=True)
    python_path.write_text("")

    def failing_iterdir(self: Path) -> Never:  # pragma: no cover - exercised when permissions fail
        raise PermissionError("denied")

    monkeypatch.setattr(lc.Path, "iterdir", failing_iterdir)

    structure = _analyze_cache_structure(python_path)
    assert structure["contents"] == ["<access_denied>"]


def test_log_launch_context_default_logger(monkeypatch: pytest.MonkeyPatch) -> None:
    context = LaunchContext(
        method=LaunchMethod.UNKNOWN,
        executable_path="/bin/app",
        python_executable="/usr/bin/python",
        working_directory="/tmp",
        environment_info={},
        is_terraform_invoked=False,
        details={},
    )
    monkeypatch.setattr(lc, "detect_launch_context", lambda: context)

    buffer = StringIO()
    with redirect_stdout(buffer):
        result = log_launch_context()

    assert result is context
    output = buffer.getvalue()
    assert "Pyvider Launch Context" in output


# 🐍🏗️🔚
