#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the release-time lint API verifier."""

import asyncio
from pathlib import Path
import zipfile

import pytest

import pyvider
from scripts.verify_lint_release import (
    REQUIRED_WHEEL_PATHS,
    verify_installed,
    verify_lint_behavior,
    verify_wheel,
)


def write_wheel(tmp_path: Path, names: set[str]) -> Path:
    wheel = tmp_path / "pyvider-0.8.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        for name in names:
            archive.writestr(name, "")
    return wheel


def test_wheel_requires_every_lint_module(tmp_path: Path) -> None:
    wheel = write_wheel(tmp_path, REQUIRED_WHEEL_PATHS - {"pyvider/lint/model.py"})
    with pytest.raises(SystemExit, match=r"pyvider/lint/model\.py"):
        verify_wheel(wheel)


def test_complete_wheel_contract_passes(tmp_path: Path) -> None:
    verify_wheel(write_wheel(tmp_path, REQUIRED_WHEEL_PATHS))


def test_installed_contract_runs_one_selected_finding() -> None:
    result = asyncio.run(verify_lint_behavior())
    assert result == {"version": pyvider.__version__, "findings": 1, "failed": False}


def test_installed_contract_rejects_version_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pyvider, "__version__", "0.0.0")
    with pytest.raises(SystemExit, match=r"expected 0\.8\.0"):
        asyncio.run(verify_installed(expected_version="0.8.0"))
