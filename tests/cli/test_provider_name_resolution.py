#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for provider-name resolution across its accepted config locations.

The name decides the Terraform plugin directory
(``~/.terraform.d/plugins/local/providers/<name>/...``), so resolving it wrongly
does not fail loudly -- it installs a working provider under a name nothing
asks for, and Terraform quietly resolves some other binary instead.
"""

from pathlib import Path
from typing import Any

import pytest

from pyvider.cli.context import PyviderContext


@pytest.fixture
def project(tmp_path: Path, monkeypatch: Any) -> Path:
    """An empty project directory that is the process's cwd."""
    monkeypatch.delenv("PYVIDER_PROVIDER_NAME", raising=False)
    monkeypatch.delenv("PYVIDER_CONFIG_FILE", raising=False)
    monkeypatch.chdir(tmp_path)
    return tmp_path


class TestPyprojectSpellings:
    """Both key spellings are read, in both sections."""

    @pytest.mark.parametrize("section", ["tool.pyvider", "pyvider"])
    @pytest.mark.parametrize("key", ["name", "provider_name"])
    def test_key_is_read(self, project: Path, section: str, key: str) -> None:
        (project / "pyproject.toml").write_text(f'[{section}]\n{key} = "myprovider"\n')
        assert PyviderContext().provider_name == "myprovider"

    def test_canonical_key_wins_over_alias(self, project: Path) -> None:
        (project / "pyproject.toml").write_text(
            '[tool.pyvider]\nname = "canonical"\nprovider_name = "alias"\n'
        )
        assert PyviderContext().provider_name == "canonical"

    def test_tool_section_wins_over_top_level(self, project: Path) -> None:
        """`[tool.pyvider]` is the PEP 518 location, so it outranks `[pyvider]`."""
        (project / "pyproject.toml").write_text(
            '[pyvider]\nname = "toplevel"\n\n[tool.pyvider]\nname = "scoped"\n'
        )
        assert PyviderContext().provider_name == "scoped"

    def test_empty_string_is_not_a_name(self, project: Path) -> None:
        (project / "pyproject.toml").write_text('[tool.pyvider]\nname = ""\n')
        assert PyviderContext().provider_name == "pyvider"


class TestPyviderToml:
    """`pyvider.toml` is read from the cwd, not only via PYVIDER_CONFIG_FILE."""

    @pytest.mark.parametrize("key", ["name", "provider_name"])
    def test_cwd_pyvider_toml_is_read(self, project: Path, key: str) -> None:
        (project / "pyvider.toml").write_text(f'[pyvider]\n{key} = "fromtoml"\n')
        assert PyviderContext().provider_name == "fromtoml"

    def test_config_file_env_var_is_read(self, project: Path, monkeypatch: Any) -> None:
        elsewhere = project / "cfg" / "pyvider.toml"
        elsewhere.parent.mkdir()
        elsewhere.write_text('[pyvider]\nname = "fromenvfile"\n')
        monkeypatch.setenv("PYVIDER_CONFIG_FILE", str(elsewhere))
        assert PyviderContext().provider_name == "fromenvfile"

    def test_pyvider_toml_without_a_name_falls_through(self, project: Path) -> None:
        """The shipped pyvider.toml has no `[pyvider]` table; it must not shadow."""
        (project / "pyvider.toml").write_text('[logging]\nlevel = "DEBUG"\n')
        (project / "pyproject.toml").write_text('[tool.pyvider]\nname = "frompyproject"\n')
        assert PyviderContext().provider_name == "frompyproject"


class TestPrecedence:
    """env > pyvider.toml > pyproject `[tool.pyvider]` > pyproject `[pyvider]`."""

    def test_env_var_beats_every_file(self, project: Path, monkeypatch: Any) -> None:
        (project / "pyvider.toml").write_text('[pyvider]\nname = "fromtoml"\n')
        (project / "pyproject.toml").write_text('[tool.pyvider]\nname = "frompyproject"\n')
        monkeypatch.setenv("PYVIDER_PROVIDER_NAME", "fromenv")
        assert PyviderContext().provider_name == "fromenv"

    def test_pyvider_toml_beats_pyproject(self, project: Path) -> None:
        (project / "pyvider.toml").write_text('[pyvider]\nname = "fromtoml"\n')
        (project / "pyproject.toml").write_text('[tool.pyvider]\nname = "frompyproject"\n')
        assert PyviderContext().provider_name == "fromtoml"


class TestSourceReporting:
    """The resolved name carries where it came from, so `install` can show it."""

    def test_default_is_labelled_as_such(self, project: Path) -> None:
        ctx = PyviderContext()
        assert ctx.provider_name == "pyvider"
        assert ctx.provider_name_source == "default"

    def test_configured_name_names_its_source(self, project: Path) -> None:
        (project / "pyproject.toml").write_text('[tool.pyvider]\nname = "configured"\n')
        ctx = PyviderContext()
        assert ctx.provider_name_source != "default"
        assert "[tool.pyvider]" in ctx.provider_name_source

    def test_env_var_source_names_the_variable(self, project: Path, monkeypatch: Any) -> None:
        monkeypatch.setenv("PYVIDER_PROVIDER_NAME", "fromenv")
        assert PyviderContext().provider_name_source == "PYVIDER_PROVIDER_NAME"


class TestPluginPath:
    """The whole point of the name: it selects the plugin directory."""

    def test_name_selects_the_plugin_directory(self, project: Path) -> None:
        (project / "pyproject.toml").write_text('[tool.pyvider]\nname = "tofusoup"\n')
        ctx = PyviderContext()
        assert "/providers/tofusoup/" in str(ctx.tf_plugin_dir).replace("\\", "/")


class TestMalformedConfig:
    """Unreadable config falls back rather than crashing the CLI."""

    def test_unparseable_pyproject_falls_back(self, project: Path) -> None:
        (project / "pyproject.toml").write_text("[tool.pyvider\nname = ")
        assert PyviderContext().provider_name == "pyvider"

    def test_non_table_section_falls_back(self, project: Path) -> None:
        (project / "pyproject.toml").write_text('[tool]\npyvider = "not-a-table"\n')
        assert PyviderContext().provider_name == "pyvider"


# 🐍🏗️🔚
