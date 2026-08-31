#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The dev-mode wrapper must hand the provider Terraform's working directory.

Terraform launches the provider as a subprocess, and the provider inherits
Terraform's working directory. Anything the wrapper does to that directory is
visible to practitioners as paths resolving somewhere they never named:

* every relative path in a configuration -- ``path.module``, ``./file`` --
* the filesystem state store's default root, ``Path.cwd() / .pyvider/state``
"""

from pathlib import Path
import subprocess
import sys
from typing import Any

import pytest

from pyvider.cli.context import PyviderContext
from pyvider.cli.utils import _place_terraform_provider_script

#: The development-mode wrapper is a bash script that sources `venv/bin/activate`
#: -- a POSIX layout `pyvider install` only ever writes. Windows cannot execute
#: it (WinError 193), so the cases that run it are skipped there; the case that
#: inspects the generated text still runs everywhere.
posix_only = pytest.mark.skipif(sys.platform == "win32", reason="dev-mode wrapper is a POSIX shell script")


@pytest.fixture
def project(tmp_path: Path, monkeypatch: Any) -> Path:
    """A provider checkout with a venv whose `pyvider` reports its cwd."""
    monkeypatch.delenv("PYVIDER_PROVIDER_NAME", raising=False)
    monkeypatch.delenv("PYVIDER_CONFIG_FILE", raising=False)
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))

    checkout = tmp_path / "checkout"
    bin_dir = checkout / ".venv" / "bin"
    bin_dir.mkdir(parents=True)
    (bin_dir / "python").write_text("#!/bin/sh\nexit 0\n")
    (bin_dir / "python").chmod(0o755)
    # `source activate` normally puts the venv on PATH; the stub does only that.
    (bin_dir / "activate").write_text(f'PATH="{bin_dir}:$PATH"\nexport PATH\n')
    # Stands in for the real entry point, reporting what it was handed.
    (bin_dir / "pyvider").write_text(
        '#!/bin/sh\necho "CWD=$(pwd)"\necho "CONFIG=${PYVIDER_CONFIG_FILE:-<unset>}"\n'
    )
    (bin_dir / "pyvider").chmod(0o755)
    (checkout / "pyproject.toml").write_text('[tool.pyvider]\nname = "demo"\n')
    (checkout / "VERSION").write_text("1.2.3")

    monkeypatch.chdir(checkout)
    return checkout


def _generate(checkout: Path) -> Path:
    ctx = PyviderContext()
    _place_terraform_provider_script(ctx)
    return ctx.tf_plugin_dir / f"terraform-provider-{ctx.provider_name}"


def _run_from(script: Path, cwd: Path) -> dict[str, str]:
    result = subprocess.run([str(script)], cwd=cwd, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stderr
    return dict(line.split("=", 1) for line in result.stdout.strip().splitlines() if "=" in line)


class TestWorkingDirectory:
    @posix_only
    def test_callers_directory_is_preserved(self, project: Path, tmp_path: Path) -> None:
        """The provider runs where Terraform ran, not where it was installed."""
        script = _generate(project)
        tf_dir = tmp_path / "terraform-workspace"
        tf_dir.mkdir()

        reported = _run_from(script, tf_dir)

        assert Path(reported["CWD"]).resolve() == tf_dir.resolve()
        assert Path(reported["CWD"]).resolve() != project.resolve()

    def test_wrapper_runs_no_cd_command(self, project: Path) -> None:
        """Guard the mechanism, not just the symptom.

        Checks executable lines only -- the script explains the absent `cd` in a
        comment, and prose should not fail a test about behaviour.
        """
        script = _generate(project)
        commands = [
            line.strip()
            for line in script.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        assert not [c for c in commands if c.startswith("cd ")], commands


class TestConfigStillFound:
    """Dropping the `cd` must not lose the provider's own configuration."""

    @posix_only
    def test_config_is_anchored_to_the_checkout(self, project: Path, tmp_path: Path) -> None:
        """pyvider.toml lives beside the provider, not beside the .tf files."""
        (project / "pyvider.toml").write_text('[logging]\nlevel = "DEBUG"\n')
        script = _generate(project)
        tf_dir = tmp_path / "elsewhere"
        tf_dir.mkdir()

        reported = _run_from(script, tf_dir)

        assert Path(reported["CONFIG"]) == project / "pyvider.toml"

    @posix_only
    def test_no_config_file_means_no_override(self, project: Path, tmp_path: Path) -> None:
        """Absent a pyvider.toml, nothing is pinned and discovery stays default."""
        script = _generate(project)
        tf_dir = tmp_path / "elsewhere2"
        tf_dir.mkdir()

        reported = _run_from(script, tf_dir)

        assert reported["CONFIG"] == "<unset>"


# 🐍🏗️🔚
