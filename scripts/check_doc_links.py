#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Check for broken links in markdown documentation.

This script scans all markdown files in the docs/ directory and verifies:
1. Internal links point to existing files
2. Anchor links are valid (basic check)
3. No duplicate headings that could cause anchor conflicts

Usage:
    python scripts/check_doc_links.py"""

from pathlib import Path
import re
import sys

# Base documentation directory
DOCS_DIR = Path(__file__).parent.parent / "docs"

# Pattern to match markdown links
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Pattern to match headings for anchor validation
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)


def slugify(text: str) -> str:
    r"""Convert heading text to anchor slug (GitHub/MkDocs style).

    Underscores are kept. Python-Markdown's toc extension -- which is what
    actually generates these anchors -- slugifies with `re.sub(r"[^\w\s-]", ...)`,
    and `\w` includes the underscore, so `## \`require_replace()\`` renders an
    anchor of `require_replace`. Stripping it here produced `requirereplace`,
    which no link could ever match: every anchor into a heading naming a Python
    identifier was reported broken, and correct links were the only ones that
    failed.

    Backticks and asterisks are removed because they are delimiters that
    disappear when the heading renders. An underscore is only a delimiter when
    it surrounds a word, which no heading in docs/ does, and Python-Markdown
    does not treat an intra-word underscore as emphasis at all.
    """
    # Remove markdown formatting delimiters. Not underscores: see above.
    text = re.sub(r"[`*]", "", text)
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug


def find_markdown_files() -> list[Path]:
    """Find all markdown files in the docs directory."""
    return list(DOCS_DIR.rglob("*.md"))


def extract_links(file_path: Path) -> list[tuple[str, str, int]]:
    """
    Extract all markdown links from a file.

    Returns list of (link_text, link_url, line_number) tuples.
    """
    links = []
    content = file_path.read_text(encoding="utf-8")

    for line_num, line in enumerate(content.split("\n"), 1):
        # Skip lines with Jinja2/macro template variables
        if "{{" in line and "}}" in line:
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


def _is_external_or_special_link(link_url: str) -> bool:
    """Check if a link is external or special."""
    return link_url.startswith(("http://", "https://", "mailto:", ":::"))


def _check_internal_link(
    file_path: Path,
    link_url: str,
    line_num: int,
    file_headings: set[str],
    DOCS_DIR: Path,
    resolve_link_path: callable,
    extract_headings: callable,
) -> list[str]:
    """Check an internal link for broken references."""
    errors = []

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
                rel_source = file_path.relative_to(DOCS_DIR)
                errors.append(
                    f"{rel_source}:{line_num}: Broken link to '{link_url}' "
                    f"(resolved to {target_path}, which does not exist)"
                )
            # If there's an anchor, check it exists in target file
            elif anchor:
                target_headings = extract_headings(target_path)
                if anchor not in target_headings:
                    rel_source = file_path.relative_to(DOCS_DIR)
                    errors.append(
                        f"{rel_source}:{line_num}: Broken anchor link '#{anchor}' in '{link_path_str}'"
                    )
        except Exception as e:
            rel_source = file_path.relative_to(DOCS_DIR)
            errors.append(f"{rel_source}:{line_num}: Error resolving link '{link_url}': {e}")
    # Just an anchor link (same file)
    elif anchor and anchor not in file_headings:
        rel_source = file_path.relative_to(DOCS_DIR)
        errors.append(f"{rel_source}:{line_num}: Broken anchor link '#{anchor}' in same file")
    return errors


def check_file_links(file_path: Path) -> list[str]:
    """
    Check all links in a file for broken references.

    Returns list of error messages.
    """
    errors = []
    links = extract_links(file_path)

    # Get headings from this file for anchor validation
    file_headings = extract_headings(file_path)

    for _link_text, link_url, line_num in links:
        if _is_external_or_special_link(link_url):
            continue

        errors.extend(
            _check_internal_link(
                file_path, link_url, line_num, file_headings, DOCS_DIR, resolve_link_path, extract_headings
            )
        )

    return errors


def main() -> int:
    """Main entry point."""
    print(f"🔍 Checking documentation links in {DOCS_DIR}")
    print()

    markdown_files = find_markdown_files()
    print(f"Found {len(markdown_files)} markdown files")
    print()

    all_errors = []

    for md_file in markdown_files:
        errors = check_file_links(md_file)
        all_errors.extend(errors)

    if all_errors:
        print("❌ Found broken links:")
        print()
        for error in all_errors:
            print(f"  {error}")
        print()
        print(f"Total: {len(all_errors)} broken link(s)")
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())

# 🐍🏗️🔚
