#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Documentation validation script for provide.io ecosystem.

This script provides commands to validate documentation configuration,
structure, and links across all projects in the provide.io ecosystem.

Usage:
    python scripts/docs_validate.py verify-config
    python scripts/docs_validate.py check-structure
    python scripts/docs_validate.py verify-links
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Base paths
SCRIPT_DIR = Path(__file__).parent
FOUNDRY_DIR = SCRIPT_DIR.parent
ECOSYSTEM_ROOT = FOUNDRY_DIR.parent

# Expected projects with documentation
EXPECTED_PROJECTS = [
    "provide-foundation",
    "provide-testkit",
    "pyvider",
    "pyvider-cty",
    "pyvider-hcl",
    "pyvider-rpcplugin",
    "pyvider-components",
    "flavorpack",
    "wrknv",
    "plating",
    "tofusoup",
    "supsrc",
]

# Pattern to match markdown links
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Pattern to match headings
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)


def slugify(text: str) -> str:
    """Convert heading text to anchor slug (GitHub/MkDocs style)."""
    # Remove markdown formatting
    text = re.sub(r"[`*_]", "", text)
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug


def verify_config() -> int:
    """Verify mkdocs.yml configuration files across projects.

    Checks:
    - mkdocs.yml exists in expected projects
    - INHERIT directive points to correct base config
    - Required fields are present
    """
    print("🔍 Verifying documentation configuration...")
    print()

    errors: list[str] = []
    warnings: list[str] = []

    for _project_name, project_warnings, project_errors in _validate_project_configs():
        warnings.extend(project_warnings)
        errors.extend(project_errors)

    # Print results
    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"  {warning}")
        print()

    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  {error}")
        print()
        print(f"Total: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"✅ All configurations valid ({len(warnings)} warning(s))")
    return 0


def _validate_project_configs() -> list[tuple[str, list[str], list[str]]]:
    """Return warnings and errors for each project's mkdocs.yml."""
    results: list[tuple[str, list[str], list[str]]] = []
    required_fields = ["site_name:", "site_url:", "dev_addr:"]

    for project_name in EXPECTED_PROJECTS:
        project_path = ECOSYSTEM_ROOT / project_name
        mkdocs_path = project_path / "mkdocs.yml"
        project_warnings: list[str] = []
        project_errors: list[str] = []

        if not project_path.exists():
            project_warnings.append(f"{project_name}: Project directory not found (skipping)")
        elif not mkdocs_path.exists():
            project_warnings.append(f"{project_name}: No mkdocs.yml found")
        else:
            try:
                content = mkdocs_path.read_text(encoding="utf-8")
            except Exception as exc:  # pragma: no cover - filesystem issue
                project_errors.append(f"{project_name}: Error reading mkdocs.yml: {exc}")
            else:
                if "INHERIT:" not in content:
                    project_errors.append(
                        f"{project_name}: Missing INHERIT directive in mkdocs.yml"
                    )
                elif ".provide/foundry/base-mkdocs.yml" not in content:
                    project_errors.append(
                        f"{project_name}: INHERIT directive does not point to "
                        ".provide/foundry/base-mkdocs.yml"
                    )

                for field in required_fields:
                    if field not in content:
                        project_errors.append(
                            f"{project_name}: Missing required field '{field}' in mkdocs.yml"
                        )

        results.append((project_name, project_warnings, project_errors))

    return results


def check_structure() -> int:
    """Check documentation directory structure across projects.

    Checks:
    - docs/ directory exists
    - docs/index.md exists
    - No planning documents in docs/ (PLAN.md, TODO.md, etc.)
    - No session files in docs/ (HANDOFF_*, PHASE_*, etc.)
    """
    print("🔍 Checking documentation structure...")
    print()

    errors: list[str] = []
    warnings: list[str] = []

    for project_warnings, project_errors in _inspect_project_structure():
        warnings.extend(project_warnings)
        errors.extend(project_errors)

    # Print results
    if warnings:
        print("⚠️  Warnings:")
        for warning in warnings:
            print(f"  {warning}")
        print()

    if errors:
        print("❌ Structure errors:")
        for error in errors:
            print(f"  {error}")
        print()
        print(f"Total: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"✅ All structures valid ({len(warnings)} warning(s))")
    return 0


def _inspect_project_structure() -> list[tuple[list[str], list[str]]]:
    """Return warnings and errors for documentation directory layout."""
    results: list[tuple[list[str], list[str]]] = []
    planning_patterns = ["PLAN.md", "TODO.md", "STRATEGY.md", "CHECKLIST.md", "DESIGN_*.md"]
    session_patterns = ["HANDOFF_*.md", "PHASE_*.md", "LLM_*.md", "*_SESSION.md"]

    for project_name in EXPECTED_PROJECTS:
        project_path = ECOSYSTEM_ROOT / project_name
        docs_path = project_path / "docs"
        warnings: list[str] = []
        errors: list[str] = []

        if not project_path.exists():
            warnings.append(f"{project_name}: Project directory not found (skipping)")
        elif not docs_path.exists():
            warnings.append(f"{project_name}: No docs/ directory found")
        else:
            if not (docs_path / "index.md").exists():
                errors.append(f"{project_name}: Missing docs/index.md")

            for pattern in planning_patterns:
                for match in docs_path.glob(pattern):
                    rel_path = match.relative_to(project_path)
                    errors.append(
                        f"{project_name}: Planning document found in docs/: {rel_path} "
                        "(should be in .dev/)"
                    )

            for pattern in session_patterns:
                for match in docs_path.rglob(pattern):
                    rel_path = match.relative_to(project_path)
                    errors.append(
                        f"{project_name}: Session file found in docs/: {rel_path} "
                        "(should be in .archive/)"
                    )

        results.append((warnings, errors))

    return results


def extract_links(file_path: Path) -> list[tuple[str, str, int]]:
    """Extract all markdown links from a file.

    Returns list of (link_text, link_url, line_number) tuples.
    """
    links = []
    content = file_path.read_text(encoding="utf-8")

    for line_num, line in enumerate(content.split("\n"), 1):
        # Skip lines with Jinja2/macro template variables
        if "{{" in line and "}}" in line:
            continue
        if "{$" in line and "$}" in line:
            continue

        for match in LINK_PATTERN.finditer(line):
            link_text = match.group(1)
            link_url = match.group(2)
            links.append((link_text, link_url, line_num))

    return links


def extract_headings(file_path: Path) -> set[str]:
    """Extract all heading slugs from a file."""
    content = file_path.read_text(encoding="utf-8")
    headings = set()

    for match in HEADING_PATTERN.finditer(content):
        heading_text = match.group(1)
        slug = slugify(heading_text)
        headings.add(slug)

    return headings


def is_external_or_special_link(link_url: str) -> bool:
    """Check if a link is external or special."""
    return link_url.startswith(("http://", "https://", "mailto:", ":::", "!include"))


def resolve_link_path(source_file: Path, link_url: str) -> Path:
    """Resolve a relative link to an absolute path."""
    # Remove anchor if present
    link_path = link_url.split("#")[0]

    if not link_path:  # Just an anchor
        return source_file

    # Resolve relative to source file's directory
    source_dir = source_file.parent
    resolved = (source_dir / link_path).resolve()

    return resolved


def check_file_links(file_path: Path, docs_dir: Path) -> list[str]:
    """Check all links in a file for broken references.

    Returns list of error messages.
    """
    errors = []
    links = extract_links(file_path)

    # Get headings from this file for anchor validation
    file_headings = extract_headings(file_path)

    for _link_text, link_url, line_num in links:
        if is_external_or_special_link(link_url):
            continue

        # Parse link and anchor
        if "#" in link_url:
            link_path_str, anchor = link_url.split("#", 1)
        else:
            link_path_str = link_url
            anchor = None

        # Check file exists (if not just an anchor)
        if link_path_str:
            try:
                target_path = resolve_link_path(file_path, link_url)

                if not target_path.exists():
                    rel_source = file_path.relative_to(docs_dir)
                    errors.append(
                        f"{rel_source}:{line_num}: Broken link to '{link_url}' "
                        f"(resolved to {target_path}, which does not exist)"
                    )
                else:
                    # If there's an anchor, check it exists in target file
                    if anchor:
                        target_headings = extract_headings(target_path)
                        if anchor not in target_headings:
                            rel_source = file_path.relative_to(docs_dir)
                            errors.append(
                                f"{rel_source}:{line_num}: Broken anchor link "
                                f"'#{anchor}' in '{link_path_str}'"
                            )
            except Exception as e:
                rel_source = file_path.relative_to(docs_dir)
                errors.append(f"{rel_source}:{line_num}: Error resolving link '{link_url}': {e}")
        else:
            # Just an anchor link (same file)
            if anchor and anchor not in file_headings:
                rel_source = file_path.relative_to(docs_dir)
                errors.append(
                    f"{rel_source}:{line_num}: Broken anchor link '#{anchor}' in same file"
                )

    return errors


def verify_links() -> int:
    """Verify internal links in documentation across all projects.

    Checks:
    - Internal file links point to existing files
    - Anchor links point to valid headings
    - No broken cross-references
    """
    print("🔍 Verifying documentation links...")
    print()

    all_errors = []
    projects_checked = 0

    for project_name in EXPECTED_PROJECTS:
        project_path = ECOSYSTEM_ROOT / project_name
        docs_path = project_path / "docs"

        if not project_path.exists():
            continue

        if not docs_path.exists():
            continue

        # Find all markdown files
        markdown_files = list(docs_path.rglob("*.md"))
        if not markdown_files:
            continue

        projects_checked += 1
        print(f"  Checking {project_name}: {len(markdown_files)} files")

        # Check each file
        for md_file in markdown_files:
            errors = check_file_links(md_file, docs_path)
            # Prepend project name to errors for context
            errors = [f"{project_name}: {error}" for error in errors]
            all_errors.extend(errors)

    print()

    if all_errors:
        print("❌ Found broken links:")
        print()
        for error in all_errors:
            print(f"  {error}")
        print()
        print(f"Total: {len(all_errors)} broken link(s) across {projects_checked} project(s)")
        return 1

    print(f"✅ All links valid across {projects_checked} project(s)")
    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate documentation configuration, structure, and links"
    )
    parser.add_argument(
        "command",
        choices=["verify-config", "check-structure", "verify-links"],
        help="Validation command to run",
    )

    args = parser.parse_args()

    if args.command == "verify-config":
        return verify_config()
    elif args.command == "check-structure":
        return check_structure()
    elif args.command == "verify-links":
        return verify_links()
    else:
        print(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
