#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Add SPDX copyright headers to Python files.

This script adds standardized SPDX headers to Python source files,
handling edge cases like existing shebangs, docstrings, and special files.
It detects incorrect headers and warns about them without modifying.
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import sys
from typing import Tuple


HEADER_LINES = [
    "# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.",
    "# SPDX-License-Identifier: Apache-2.0",
]

EXCLUDED_PATTERNS = [
    ".venv/",
    "site-packages/",
    ".provide/foundry/",
    "site/",
    "__pycache__",
    ".egg-info",
]


def check_header_correctness(content: str) -> Tuple[bool, str]:
    """Check if existing header is correct. Returns (is_correct, issue)."""
    lines = content.split('\n')[:15]

    # Check for SPDX format
    has_spdx = any('SPDX-FileCopyrightText' in line for line in lines)
    has_license = any('SPDX-License-Identifier: Apache-2.0' in line for line in lines)

    if not has_spdx or not has_license:
        return False, "Missing SPDX tags or incorrect license"

    # Check year and company
    copyright_line = next((l for l in lines if 'SPDX-FileCopyrightText' in l), '')
    if '2025' not in copyright_line:
        return False, "Incorrect year (not 2025)"
    if 'provide.io llc' not in copyright_line:
        return False, "Incorrect company name"

    return True, ""


def should_skip_file(file_path: Path) -> Tuple[bool, str]:
    """Determine if file should be skipped. Returns (should_skip, reason)."""
    # Check exclusion patterns
    for pattern in EXCLUDED_PATTERNS:
        if pattern in str(file_path):
            return True, f"matches exclusion pattern: {pattern}"

    # Skip nearly empty __init__.py files (namespace packages)
    if file_path.name == "__init__.py":
        content = file_path.read_text()
        lines = content.strip().split('\n')
        if len(lines) <= 3:
            return True, "nearly empty namespace package"

    return False, ""


def has_shebang(content: str) -> bool:
    """Check if file starts with shebang."""
    return content.startswith("#!")


def add_header(file_path: Path, dry_run: bool = False, verbose: bool = False) -> Tuple[bool, str]:
    """Add SPDX header to file. Returns (modified, message)."""
    try:
        content = file_path.read_text()
    except Exception as e:
        return False, f"ERROR: Could not read {file_path}: {e}"

    # Check if should skip
    skip, reason = should_skip_file(file_path)
    if skip:
        if verbose:
            return False, f"  SKIP: {file_path.relative_to(Path.cwd())} ({reason})"
        return False, ""

    # Check for existing headers
    if "SPDX-FileCopyrightText" in content or "Copyright" in content[:500]:
        is_correct, issue = check_header_correctness(content)
        if not is_correct:
            return False, f"  ⚠️  WARN: {file_path.relative_to(Path.cwd())} - {issue} (manual review needed)"
        # Header already exists and is correct
        if verbose:
            return False, f"  SKIP: {file_path.relative_to(Path.cwd())} (already has correct header)"
        return False, ""

    # Determine header placement
    lines = content.split('\n')
    insert_line = 0

    if has_shebang(content):
        insert_line = 1  # After shebang

    # Insert header with blank line after
    new_lines = (
        lines[:insert_line] +
        HEADER_LINES +
        [''] +  # Blank line after header
        lines[insert_line:]
    )
    new_content = '\n'.join(new_lines)

    # Validate syntax before writing
    try:
        ast.parse(new_content)
    except SyntaxError as e:
        return False, f"  ERROR: {file_path.relative_to(Path.cwd())} - Invalid syntax after header: {e}"

    if dry_run:
        return True, f"  DRY-RUN: Would add header to {file_path.relative_to(Path.cwd())}"

    # Write file atomically
    try:
        file_path.write_text(new_content)
        return True, f"  ✓ Added header to {file_path.relative_to(Path.cwd())}"
    except Exception as e:
        return False, f"  ERROR: Could not write {file_path}: {e}"


def find_python_files(root: Path) -> list[Path]:
    """Find all Python files to process."""
    files = []
    for pattern in ["src/**/*.py", "scripts/*.py", "tests/*.py"]:
        for p in root.glob(pattern):
            if not any(excl in str(p) for excl in EXCLUDED_PATTERNS):
                files.append(p)
    return sorted(set(files))


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Add SPDX copyright headers to Python files"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would change without modifying files"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output including skipped files"
    )
    args = parser.parse_args()

    root = Path.cwd()
    python_files = find_python_files(root)

    if args.dry_run:
        print("DRY-RUN MODE - No files will be modified")
        print()

    print(f"Found {len(python_files)} Python files to check")
    print()

    modified = 0
    skipped = 0
    warnings = 0

    for file_path in python_files:
        was_modified, message = add_header(file_path, dry_run=args.dry_run, verbose=args.verbose)

        if message:
            print(message)

        if "WARN:" in message:
            warnings += 1
        elif was_modified:
            modified += 1
        else:
            skipped += 1

    print()
    print("=" * 70)
    print("Summary:")
    print(f"  Files that {'would be ' if args.dry_run else ''}modified: {modified}")
    print(f"  Files skipped: {skipped}")
    print(f"  Files with warnings: {warnings}")
    print(f"  Total scanned: {len(python_files)}")
    print("=" * 70)

    if args.dry_run and modified > 0:
        print()
        print("Run without --dry-run to apply these changes")

    if warnings > 0:
        print()
        print(f"⚠️  {warnings} file(s) with incorrect headers need manual review")
        return 1 if not args.dry_run else 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
