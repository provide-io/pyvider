#
# SPDX-FileCopyrightText: Copyright (c) 2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Contracts for repository task-runner commands."""

from pathlib import Path
import shlex
import tomllib

ROOT = Path(__file__).parents[2]


def test_docs_build_runs_mkdocs_in_the_uv_project_environment() -> None:
    config = tomllib.loads((ROOT / "wrknv.toml").read_text(encoding="utf-8"))
    command = config["tasks"]["docs"]["build"]
    mkdocs_command = next(part.strip() for part in command.split("&&") if "mkdocs" in part)

    assert shlex.split(mkdocs_command)[:3] == ["uv", "run", "mkdocs"]
