#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI utility helpers."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from pyvider.cli.utils import _place_terraform_provider_script


def test_place_terraform_provider_script(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    plugin_dir = tmp_path / "plugins"
    ctx = SimpleNamespace(tf_plugin_dir=plugin_dir, provider_name="pyvider")
    install_dir = tmp_path / "project"
    install_dir.mkdir()

    # Create a fake venv directory structure
    venv_dir = install_dir / ".venv"
    venv_bin = venv_dir / "bin"
    venv_bin.mkdir(parents=True)
    (venv_bin / "python").touch()
    (venv_bin / "pyvider").touch()
    (venv_bin / "activate").touch()  # Required by _find_actual_venv

    monkeypatch.setattr("pyvider.cli.utils.Path.cwd", lambda: install_dir)

    captured: dict[str, str] = {}

    def fake_atomic(path: Path, content: str) -> None:
        captured["path"] = str(path)
        captured["content"] = content
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    monkeypatch.setattr("pyvider.cli.utils.atomic_write_text", fake_atomic)
    monkeypatch.setattr("pyvider.cli.utils.pout", lambda *args, **kwargs: None)

    _place_terraform_provider_script(ctx)

    target_path = plugin_dir / "terraform-provider-pyvider"
    assert captured["path"] == str(target_path)
    assert target_path.exists()
    assert f'INSTALL_DIR="{install_dir}"' in captured["content"]
    assert 'exec pyvider "$@"' in captured["content"]


# 🐍🏗️🔚
