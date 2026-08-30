#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Report capped or exact dependency pins across the core pyvider suite.

The suite's policy is floor-only constraints: a cap turns a loud, fixable
failure into a silent refusal to upgrade, and outlives whatever it went up for.
Run this to confirm the policy still holds.

Not yet wired into CI: gating a suite-dependency-refresh check on this script
is a decision that has not been made yet. Run it manually until that decision
lands.

Usage::

    # audit the sibling checkouts next to this repo
    python scripts/audit_pins.py

    # audit a different suite checkout
    python scripts/audit_pins.py --suite-root ~/code/pyv
    PYVIDER_SUITE_ROOT=~/code/pyv python scripts/audit_pins.py
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tomllib

from provide.foundation import perr, pout

REPO_ROOT = Path(__file__).resolve().parent.parent

# The suite checkout this repo normally lives in has every sibling as a
# directory alongside this one -- so absent an explicit override, the parent
# of this repo *is* the suite root.
DEFAULT_SUITE_ROOT = REPO_ROOT.parent

SUITE_ROOT_ENV_VAR = "PYVIDER_SUITE_ROOT"

CORE = (
    "provide-foundation",
    "provide-testkit",
    "pyvider-cty",
    "pyvider-rpcplugin",
    "pyvider-hcl",
    "pyvider",
    "plating",
    "pyvider-components",
    "tofusoup",
    "terraform-provider-pyvider",
)
CAPPED = ("<", "==", "~=")


def resolve_suite_root(cli_value: Path | None) -> Path:
    """Resolve the suite root from, in order: the CLI flag, the env var, the default."""
    if cli_value is not None:
        return cli_value.expanduser().resolve()
    env_value = os.environ.get(SUITE_ROOT_ENV_VAR)
    if env_value:
        return Path(env_value).expanduser().resolve()
    return DEFAULT_SUITE_ROOT


def requirements(repo_root: Path) -> list[tuple[str, str]]:
    """Yield (section, requirement) for every dependency the repo declares."""
    data = tomllib.loads((repo_root / "pyproject.toml").read_text())
    project = data.get("project", {})
    found = [("dependencies", r) for r in project.get("dependencies", [])]
    for extra, reqs in project.get("optional-dependencies", {}).items():
        found += [(f"optional:{extra}", r) for r in reqs]
    for group, reqs in data.get("dependency-groups", {}).items():
        found += [(f"group:{group}", r) for r in reqs if isinstance(r, str)]
    return found


def audit(suite_root: Path, repos: tuple[str, ...] = CORE) -> tuple[list[str], list[str]]:
    """Return (offenders, skipped) across ``repos`` found under ``suite_root``.

    A repo whose checkout is not present is skipped rather than treated as a
    failure -- a partial checkout (only some siblings cloned) must still be
    auditable for whichever repos it does have.
    """
    offenders: list[str] = []
    skipped: list[str] = []
    for repo in repos:
        repo_root = suite_root / repo
        if not (repo_root / "pyproject.toml").is_file():
            skipped.append(repo)
            continue
        for section, requirement in requirements(repo_root):
            # Environment markers after ';' may legitimately contain '<'.
            if any(token in requirement.split(";")[0] for token in CAPPED):
                offenders.append(f"{repo} [{section}] {requirement}")
    return offenders, skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--suite-root",
        type=Path,
        default=None,
        help=(
            "Directory containing the sibling repo checkouts. Defaults to "
            f"${SUITE_ROOT_ENV_VAR} if set, else the parent directory of this repo."
        ),
    )
    args = parser.parse_args(argv)

    suite_root = resolve_suite_root(args.suite_root)
    offenders, skipped = audit(suite_root)
    checked = len(CORE) - len(skipped)

    if skipped:
        pout(f"Skipped {len(skipped)} repositories not present under {suite_root}: {', '.join(skipped)}")

    if offenders:
        perr("Capped or exact pins found:")
        for offender in offenders:
            perr(f"  {offender}")
        return 1

    pout(f"No capped pins across {checked} core repositories present under {suite_root}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


# 🐍🏗️🔚
