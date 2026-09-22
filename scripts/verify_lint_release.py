#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Verify that a release wheel contains and runs the public lint API."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys
import zipfile

REQUIRED_WHEEL_PATHS = {
    "pyvider/lint/__init__.py",
    "pyvider/lint/model.py",
    "pyvider/lint/selector.py",
    "pyvider/lint/_runner.py",
    "pyvider/protocols/tfprotov6/handlers/_linting.py",
}


def _resolved_path(value: str) -> Path:
    return Path(value).resolve()


async def verify_lint_behavior() -> dict[str, object]:
    """Exercise the installed public lint model, selector, and runner."""
    import pyvider
    from pyvider.lint import LintContext, LintFinding, LintSelector
    from pyvider.lint._runner import run_lints

    class Component:
        async def lint(self, ctx: object) -> tuple[LintFinding, ...]:
            return (
                LintFinding(
                    rule="release/pyvider:smoke",
                    groups=("release/pyvider:all",),
                    summary="Release verifier finding",
                    detail="The public runner executed the installed lint hook.",
                    attribute_path="name",
                ),
            )

    selector = LintSelector.parse(("release/pyvider:all",))
    context = LintContext({"name": "release"}, selector)
    if not context.enabled("release/pyvider:smoke", "release/pyvider:all"):
        raise SystemExit("public LintContext selector contract failed")
    result = await run_lints(
        Component(),
        context.config,
        context.selector,
        kind="provider",
        name="release-smoke",
        operation="verify-release",
    )
    if result.failed or len(result.findings) != 1:
        raise SystemExit(f"unexpected lint result: {result!r}")
    return {"version": pyvider.__version__, "findings": 1, "failed": False}


async def verify_installed(*, expected_version: str) -> dict[str, object]:
    """Verify the version, origin, and lint behavior of installed Pyvider."""
    import pyvider

    if pyvider.__version__ != expected_version:
        raise SystemExit(f"expected {expected_version}, got {pyvider.__version__}")
    origin = _resolved_path(pyvider.__file__)
    if _resolved_path(sys.prefix) not in origin.parents:
        raise SystemExit(f"pyvider imported outside isolated environment: {origin}")
    result = await verify_lint_behavior()
    result["origin"] = str(origin)
    return result


def verify_wheel(path: Path) -> None:
    """Require every lint API implementation module in a wheel archive."""
    with zipfile.ZipFile(path) as archive:
        missing = REQUIRED_WHEEL_PATHS - set(archive.namelist())
    if missing:
        raise SystemExit("wheel missing: " + ", ".join(sorted(missing)))


def main(argv: list[str] | None = None) -> int:
    """Run one release verification mode from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--wheel", type=Path, help="inspect a built wheel archive")
    mode.add_argument("--expected-version", help="verify the installed distribution")
    args = parser.parse_args(argv)

    if args.wheel is not None:
        verify_wheel(args.wheel)
        return 0

    result = asyncio.run(verify_installed(expected_version=args.expected_version))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
