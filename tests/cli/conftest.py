#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Shared fixtures for the CLI tests."""

from pathlib import Path
from typing import Any

import pytest


@pytest.fixture(autouse=True)
def isolated_home(tmp_path_factory: Any, monkeypatch: Any) -> Path:
    """Point HOME at a scratch directory for every CLI test.

    `pyvider install` writes to ``Path.home() / ".terraform.d" / "plugins"``,
    and `CliRunner.isolated_filesystem` only isolates the working directory --
    so running the suite left real provider binaries in the developer's own
    plugin directory, under whatever names and versions the tests happened to
    use. Terraform resolves those, which is precisely the failure this
    directory's tests exist to prevent.
    """
    home = tmp_path_factory.mktemp("home")
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))  # Path.home() on Windows
    return home


# 🐍🏗️🔚
