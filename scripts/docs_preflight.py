#!/usr/bin/env python
"""Pre-flight checks for documentation builds."""

from __future__ import annotations

import sys
from pathlib import Path


def check_docs_ready() -> tuple[bool, list[str]]:
    """Check if documentation is ready to build."""
    issues = []

    # Check 1: provide-foundry installed
    try:
        import provide.foundry  # noqa: F401
    except ImportError:
        issues.append("provide-foundry not installed (run: uv sync)")
        return False, issues

    # Check 2: .provide/foundry/ exists
    provide_dir = Path(".provide/foundry")
    if not provide_dir.exists():
        issues.append(".provide/foundry/ missing (will auto-setup)")
        return False, issues

    # Check 3: Required files extracted
    required = [
        provide_dir / "base-mkdocs.yml",
        provide_dir / "theme",
        provide_dir / "docs/_partials",
    ]

    missing = [f.name for f in required if not f.exists()]
    if missing:
        issues.append(f"Missing extracted files: {', '.join(missing)}")
        return False, issues

    return True, []


def auto_setup() -> bool:
    """Attempt automatic setup if needed."""
    ready, issues = check_docs_ready()

    if ready:
        return True

    print("📦 First-time setup required")
    print()

    for issue in issues:
        print(f"  ❌ {issue}")

    # Try auto-setup
    if ".provide/foundry/ missing" in " ".join(issues):
        print()
        print("  Attempting automatic setup...")
        try:
            from provide.foundry.config import extract_base_mkdocs

            extract_base_mkdocs(Path("."))
            print("  ✅ Setup complete!")
            return True
        except Exception as e:
            print(f"  ❌ Auto-setup failed: {e}")
            return False

    return False


def main() -> int:
    """Run preflight checks."""
    if auto_setup():
        print("✅ Documentation ready to build")
        return 0
    else:
        print()
        print("❌ Please fix the issues above and try again")
        print()
        print("Manual setup:")
        print("  1. Run: uv sync")
        print("  2. Run: make docs-setup")
        return 1


if __name__ == "__main__":
    sys.exit(main())
