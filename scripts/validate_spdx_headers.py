#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Validate that all Python source files have SPDX copyright headers.

This script checks that all Python files in src/, scripts/, and tests/
have proper SPDX headers. It's designed to run in CI to prevent regression.

Exit codes:
  0 - All files compliant
  1 - Missing headers detected
"""

from __future__ import annotations

from pathlib import Path
import sys

EXCLUDED_PATTERNS = [
    ".venv/",
    "site-packages/",
    ".provide/foundry/",
    "site/",
    "__pycache__",
    ".egg-info",
]


def is_nearly_empty(file_path: Path) -> bool:
    """Check if __init__.py is nearly empty (skip requirement)."""
    if file_path.name == "__init__.py":
        content = file_path.read_text()
        lines = content.strip().split('\n')
        return len(lines) <= 3
    return False


def check_file_has_header(file_path: Path) -> bool:
    """Check if file has SPDX header in first 15 lines."""
    content = file_path.read_text()
    lines = content.split('\n')[:15]

    has_copyright = any('SPDX-FileCopyrightText' in line for line in lines)
    has_license = any('SPDX-License-Identifier: Apache-2.0' in line for line in lines)

    return has_copyright and has_license


def should_skip(file_path: Path) -> bool:
    """Determine if file should be skipped."""
    # Check exclusion patterns
    for pattern in EXCLUDED_PATTERNS:
        if pattern in str(file_path):
            return True

    # Skip nearly empty __init__.py files
    if is_nearly_empty(file_path):
        return True

    return False


def find_python_files(root: Path) -> list[Path]:
    """Find all Python source files to validate."""
    files = []
    for pattern in ["src/**/*.py", "scripts/*.py", "tests/*.py"]:
        for p in root.glob(pattern):
            if not should_skip(p):
                files.append(p)
    return sorted(set(files))


def main() -> int:
    """Check all Python files have SPDX headers."""
    root = Path.cwd()
    python_files = find_python_files(root)

    missing_headers = []

    for file_path in python_files:
        if not check_file_has_header(file_path):
            missing_headers.append(file_path)

    if missing_headers:
        print("❌ SPDX Header Validation Failed")
        print()
        print("The following files are missing SPDX copyright headers:")
        print()
        for file_path in missing_headers:
            rel_path = file_path.relative_to(root)
            print(f"  - {rel_path}")
        print()
        print(f"Total: {len(missing_headers)} file(s) missing headers")
        print()
        print("Run: python scripts/add_spdx_headers.py")
        return 1

    print(f"✅ All {len(python_files)} Python files have SPDX headers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
